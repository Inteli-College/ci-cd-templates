"""
Gerador de Configurações de Validação
Permite criar configurações via interface programática
"""

import yaml
import json
from typing import Dict, List, Any
from pathlib import Path

class ValidationConfigBuilder:
    """Builder para criar configurações de validação"""
    
    def __init__(self, name: str, description: str = ""):
        self.config = {
            'name': name,
            'description': description,
            'validations': {
                'folders': [],
                'files': [],
                'api_checks': [],
                'custom_scripts': []
            },
            'notification': {
                'slack': {
                    'enabled': False,
                    'channel': '',
                    'mention_on_failure': False,
                    'users_to_mention': []
                }
            }
        }
    
    def add_folder_check(self, path: str, required: bool = True, description: str = ""):
        """Adiciona verificação de pasta"""
        folder_check = {
            'path': path,
            'required': required,
            'description': description or f'Pasta {path}'
        }
        self.config['validations']['folders'].append(folder_check)
        return self
    
    def add_file_check(self, path: str, required: bool = True, description: str = "", validations: List[Dict] = None):
        """Adiciona verificação de arquivo"""
        file_check = {
            'path': path,
            'required': required,
            'description': description or f'Arquivo {path}'
        }
        
        if validations:
            file_check['validations'] = validations
            
        self.config['validations']['files'].append(file_check)
        return self
    
    def add_content_validation(self, validation_type: str, value: Any, description: str = ""):
        """Cria validação de conteúdo para ser usada com add_file_check"""
        return {
            'type': validation_type,
            'value': value,
            'description': description
        }
    
    def add_api_check(self, url: str, method: str = 'GET', required: bool = True, 
                     expected_status: int = 200, description: str = ""):
        """Adiciona verificação de API"""
        api_check = {
            'url': url,
            'method': method,
            'required': required,
            'expected_status': expected_status,
            'description': description or f'API {url}'
        }
        self.config['validations']['api_checks'].append(api_check)
        return self
    
    def add_custom_script(self, name: str, script: str, required: bool = True, description: str = ""):
        """Adiciona script personalizado"""
        script_check = {
            'name': name,
            'script': script,
            'required': required,
            'description': description or f'Script {name}'
        }
        self.config['validations']['custom_scripts'].append(script_check)
        return self
    
    def configure_slack(self, channel: str, enabled: bool = True, mention_on_failure: bool = True,
                       users_to_mention: List[str] = None):
        """Configura notificações do Slack"""
        self.config['notification']['slack'] = {
            'enabled': enabled,
            'channel': channel,
            'mention_on_failure': mention_on_failure,
            'users_to_mention': users_to_mention or []
        }
        return self
    
    def to_yaml(self) -> str:
        """Converte configuração para YAML"""
        return yaml.dump(self.config, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def to_dict(self) -> Dict:
        """Retorna configuração como dicionário"""
        return self.config.copy()
    
    def save_to_file(self, file_path: str):
        """Salva configuração em arquivo YAML"""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return file_path

# Exemplos de uso e templates predefinidos
class ValidationTemplates:
    """Templates predefinidos para diferentes tipos de projeto"""
    
    @staticmethod
    def web_application_template() -> ValidationConfigBuilder:
        """Template para aplicação web completa"""
        builder = ValidationConfigBuilder(
            name="Validação - Aplicação Web",
            description="Template para aplicação web com frontend e backend"
        )
        
        # Estrutura de pastas padrão
        builder.add_folder_check("src", True, "Pasta principal do código")
        builder.add_folder_check("src/backend", True, "Backend da aplicação")
        builder.add_folder_check("src/frontend", True, "Frontend da aplicação")
        builder.add_folder_check("docs", True, "Documentação")
        builder.add_folder_check("tests", False, "Testes automatizados")
        
        # Arquivos essenciais
        readme_validations = [
            builder.add_content_validation("content_contains", "# ", "Deve conter título principal"),
            builder.add_content_validation("min_lines", 20, "Deve ter pelo menos 20 linhas"),
            builder.add_content_validation("content_contains", "## Instalação", "Deve conter seção de instalação")
        ]
        builder.add_file_check("README.md", True, "README principal", readme_validations)
        builder.add_file_check(".gitignore", True, "Arquivo gitignore")
        builder.add_file_check("requirements.txt", False, "Dependências Python")
        builder.add_file_check("package.json", False, "Dependências Node.js")
        
        # Verificações de API
        builder.add_api_check("http://localhost:5000/health", "GET", False, 200, "Health check backend")
        builder.add_api_check("http://localhost:3000", "GET", False, 200, "Frontend acessível")
        
        # Scripts personalizados
        builder.add_custom_script("lint_python", "flake8 src/", False, "Lint do código Python")
        builder.add_custom_script("test_backend", "python -m pytest tests/", False, "Testes do backend")
        
        # Configurar Slack
        builder.configure_slack("#entregas", True, True, ["@professor"])
        
        return builder
    
    @staticmethod
    def mobile_app_template() -> ValidationConfigBuilder:
        """Template para aplicação mobile"""
        builder = ValidationConfigBuilder(
            name="Validação - Aplicação Mobile",
            description="Template para aplicação mobile React Native/Flutter"
        )
        
        builder.add_folder_check("src", True, "Código fonte")
        builder.add_folder_check("assets", True, "Recursos da aplicação")
        builder.add_folder_check("docs", True, "Documentação")
        
        readme_validations = [
            builder.add_content_validation("content_contains", "# ", "Deve conter título"),
            builder.add_content_validation("content_contains", "## Como executar", "Instruções de execução"),
            builder.add_content_validation("min_lines", 15, "Pelo menos 15 linhas")
        ]
        builder.add_file_check("README.md", True, "README principal", readme_validations)
        builder.add_file_check("package.json", True, "Configuração Node.js")
        builder.add_file_check("app.json", False, "Configuração do app")
        
        return builder
    
    @staticmethod
    def data_science_template() -> ValidationConfigBuilder:
        """Template para projeto de Data Science"""
        builder = ValidationConfigBuilder(
            name="Validação - Projeto Data Science",
            description="Template para projetos de análise de dados e ML"
        )
        
        builder.add_folder_check("notebooks", True, "Jupyter notebooks")
        builder.add_folder_check("data", True, "Datasets")
        builder.add_folder_check("src", True, "Código fonte")
        builder.add_folder_check("models", False, "Modelos treinados")
        
        builder.add_file_check("README.md", True, "Documentação principal")
        builder.add_file_check("requirements.txt", True, "Dependências Python")
        builder.add_file_check("notebooks/analise_exploratoria.ipynb", False, "Análise exploratória")
        
        builder.add_custom_script("check_datasets", "python -c 'import pandas as pd; print(\"Datasets OK\")'", False, "Verificar datasets")
        
        return builder

def create_config_from_interface(project_type: str, **kwargs) -> ValidationConfigBuilder:
    """
    Simula interface web/CLI que permite criar configurações
    Esta função seria chamada por uma interface web ou CLI
    """
    
    if project_type == "web":
        return ValidationTemplates.web_application_template()
    elif project_type == "mobile":
        return ValidationTemplates.mobile_app_template()
    elif project_type == "data_science":
        return ValidationTemplates.data_science_template()
    else:
        # Configuração personalizada
        name = kwargs.get('name', 'Projeto Personalizado')
        description = kwargs.get('description', '')
        return ValidationConfigBuilder(name, description)

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo 1: Usando template
    config = ValidationTemplates.web_application_template()
    print("=== Template Web Application ===")
    print(config.to_yaml())
    
    # Exemplo 2: Criação manual
    custom_config = ValidationConfigBuilder(
        "Meu Projeto Custom",
        "Configuração personalizada criada programaticamente"
    )
    
    custom_config.add_folder_check("src", True) \
                 .add_folder_check("tests", False) \
                 .add_file_check("README.md", True, "Documentação", [
                     custom_config.add_content_validation("min_lines", 10, "Pelo menos 10 linhas")
                 ]) \
                 .add_api_check("http://localhost:8000/api/health", "GET", False) \
                 .configure_slack("#meu-canal", True, True, ["@eu"])
    
    print("\n=== Configuração Personalizada ===")
    print(custom_config.to_yaml())
