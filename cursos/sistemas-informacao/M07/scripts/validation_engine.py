"""
Sistema de Validação Configurável
Executa validações baseadas em arquivo de configuração YAML
"""

import yaml
import os
import requests
import subprocess
import json
from pathlib import Path
from shared.utils.file_checks import file_exists, folder_exists

class ValidationEngine:
    def __init__(self, config_path):
        """Inicializa o motor de validação com arquivo de configuração"""
        self.config_path = config_path
        self.config = self.load_config()
        self.results = []
        
    def load_config(self):
        """Carrega configuração do arquivo YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise Exception(f"Erro ao carregar configuração: {e}")
    
    def validate_folders(self):
        """Valida existência de pastas"""
        if 'folders' not in self.config.get('validations', {}):
            return
            
        for folder in self.config['validations']['folders']:
            path = folder['path']
            required = folder.get('required', True)
            description = folder.get('description', f'Pasta {path}')
            
            exists = folder_exists(path)
            
            result = {
                'type': 'folder',
                'path': path,
                'description': description,
                'required': required,
                'passed': exists or not required,
                'exists': exists,
                'message': f"✅ {description}" if exists else f"❌ {description} não encontrada"
            }
            
            self.results.append(result)
    
    def validate_files(self):
        """Valida existência e conteúdo de arquivos"""
        if 'files' not in self.config.get('validations', {}):
            return
            
        for file_config in self.config['validations']['files']:
            path = file_config['path']
            required = file_config.get('required', True)
            description = file_config.get('description', f'Arquivo {path}')
            
            exists = file_exists(path)
            
            # Resultado base
            result = {
                'type': 'file',
                'path': path,
                'description': description,
                'required': required,
                'exists': exists,
                'validations': []
            }
            
            # Se arquivo existe, executa validações de conteúdo
            if exists and 'validations' in file_config:
                self.validate_file_content(path, file_config['validations'], result)
            
            # Determina se passou na validação
            content_validations_passed = all(v['passed'] for v in result['validations'])
            result['passed'] = (exists or not required) and content_validations_passed
            result['message'] = f"✅ {description}" if result['passed'] else f"❌ {description} falhou na validação"
            
            self.results.append(result)
    
    def validate_file_content(self, file_path, validations, result):
        """Valida conteúdo específico do arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.split('\n')
                
            for validation in validations:
                validation_result = self.execute_content_validation(content, lines, validation)
                result['validations'].append(validation_result)
                
        except Exception as e:
            result['validations'].append({
                'type': 'error',
                'passed': False,
                'message': f"Erro ao ler arquivo: {e}"
            })
    
    def execute_content_validation(self, content, lines, validation):
        """Executa validação específica de conteúdo"""
        validation_type = validation['type']
        expected_value = validation['value']
        description = validation.get('description', f'Validação {validation_type}')
        
        if validation_type == 'content_contains':
            passed = expected_value in content
            message = f"✅ {description}" if passed else f"❌ {description}"
            
        elif validation_type == 'min_lines':
            passed = len(lines) >= expected_value
            actual = len(lines)
            message = f"✅ {description} ({actual} linhas)" if passed else f"❌ {description} ({actual}/{expected_value} linhas)"
            
        elif validation_type == 'max_lines':
            passed = len(lines) <= expected_value
            actual = len(lines)
            message = f"✅ {description} ({actual} linhas)" if passed else f"❌ {description} ({actual}/{expected_value} linhas)"
            
        else:
            passed = False
            message = f"❌ Tipo de validação desconhecido: {validation_type}"
        
        return {
            'type': validation_type,
            'expected': expected_value,
            'passed': passed,
            'message': message,
            'description': description
        }
    
    def validate_api_endpoints(self):
        """Valida endpoints de API"""
        if 'api_checks' not in self.config.get('validations', {}):
            return
            
        for api_check in self.config['validations']['api_checks']:
            url = api_check['url']
            method = api_check.get('method', 'GET')
            required = api_check.get('required', True)
            expected_status = api_check.get('expected_status', 200)
            description = api_check.get('description', f'API {url}')
            
            try:
                response = requests.request(method, url, timeout=10)
                passed = response.status_code == expected_status
                message = f"✅ {description} ({response.status_code})" if passed else f"❌ {description} ({response.status_code}/{expected_status})"
                
            except Exception as e:
                passed = False
                message = f"❌ {description} - Erro: {str(e)}"
            
            result = {
                'type': 'api',
                'url': url,
                'method': method,
                'description': description,
                'required': required,
                'passed': passed or not required,
                'message': message
            }
            
            self.results.append(result)
    
    def run_custom_scripts(self):
        """Executa scripts personalizados"""
        if 'custom_scripts' not in self.config.get('validations', {}):
            return
            
        for script_config in self.config['validations']['custom_scripts']:
            name = script_config['name']
            script = script_config['script']
            required = script_config.get('required', True)
            description = script_config.get('description', f'Script {name}')
            
            try:
                result = subprocess.run(script, shell=True, capture_output=True, text=True, timeout=60)
                passed = result.returncode == 0
                
                message = f"✅ {description}" if passed else f"❌ {description}"
                if result.stderr:
                    message += f" - Erro: {result.stderr[:100]}"
                
            except subprocess.TimeoutExpired:
                passed = False
                message = f"❌ {description} - Timeout"
            except Exception as e:
                passed = False
                message = f"❌ {description} - Erro: {str(e)}"
            
            result = {
                'type': 'script',
                'name': name,
                'script': script,
                'description': description,
                'required': required,
                'passed': passed or not required,
                'message': message
            }
            
            self.results.append(result)
    
    def run_all_validations(self):
        """Executa todas as validações configuradas"""
        print(f"🔍 Iniciando validações: {self.config.get('name', 'Configuração sem nome')}")
        print(f"📝 {self.config.get('description', '')}")
        print("-" * 50)
        
        self.validate_folders()
        self.validate_files()
        self.validate_api_endpoints()
        self.run_custom_scripts()
        
        return self.results
    
    def generate_report(self):
        """Gera relatório das validações"""
        total_validations = len(self.results)
        passed_validations = sum(1 for r in self.results if r['passed'])
        failed_validations = total_validations - passed_validations
        
        report = {
            'summary': {
                'total': total_validations,
                'passed': passed_validations,
                'failed': failed_validations,
                'success_rate': (passed_validations / total_validations * 100) if total_validations > 0 else 0
            },
            'details': self.results,
            'config': self.config
        }
        
        return report
    
    def print_results(self):
        """Imprime resultados das validações"""
        report = self.generate_report()
        
        print("\n" + "="*50)
        print("📊 RESUMO DAS VALIDAÇÕES")
        print("="*50)
        print(f"Total: {report['summary']['total']}")
        print(f"✅ Passou: {report['summary']['passed']}")
        print(f"❌ Falhou: {report['summary']['failed']}")
        print(f"📈 Taxa de sucesso: {report['summary']['success_rate']:.1f}%")
        
        print("\n" + "-"*50)
        print("📋 DETALHES")
        print("-"*50)
        
        for result in self.results:
            print(f"{result['message']}")
            
            # Mostra detalhes de validações de conteúdo
            if 'validations' in result:
                for validation in result['validations']:
                    print(f"   └─ {validation['message']}")
        
        print("\n" + "="*50)
        
        # Retorna código de saída
        return 0 if report['summary']['failed'] == 0 else 1

def main():
    """Função principal"""
    # Determina caminho do arquivo de configuração
    config_path = os.environ.get('VALIDATION_CONFIG', 'cursos/sistemas-informacao/M07/config/validation-config.yml')
    
    if not os.path.exists(config_path):
        print(f"❌ Arquivo de configuração não encontrado: {config_path}")
        return 1
    
    try:
        # Executa validações
        engine = ValidationEngine(config_path)
        engine.run_all_validations()
        exit_code = engine.print_results()
        
        # Salvar resultados para compatibilidade com sistema de notificações
        report = engine.generate_report()
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump({
                "summary": f"{report['summary']['passed']}/{report['summary']['total']} validações passaram",
                "status": "success" if exit_code == 0 else "failed",
                "details": report['details'],
                "config": report['config'],
                "success_rate": report['summary']['success_rate']
            }, f, indent=2, ensure_ascii=False)
        
        return exit_code
        
    except Exception as e:
        print(f"❌ Erro durante execução das validações: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
