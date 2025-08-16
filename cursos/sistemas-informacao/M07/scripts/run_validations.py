#!/usr/bin/env python3
"""
Script principal para executar validações do M07
Utiliza o ValidationEngine para executar validações configuráveis via YAML
"""

import sys
import os
from validation_engine import ValidationEngine

def main():
    """Executa as validações usando o novo sistema configurável"""
    
    # Caminho para o arquivo de configuração
    config_path = 'cursos/sistemas-informacao/M07/config/validation-config.yml'
    
    print("🚀 Iniciando sistema de validação configurável")
    print(f"📋 Usando configuração: {config_path}")
    
    try:
        # Cria e executa o motor de validação
        engine = ValidationEngine(config_path)
        engine.run_all_validations()
        exit_code = engine.print_results()
        
        return exit_code
        
    except Exception as e:
        print(f"❌ Erro fatal durante execução: {e}")
        return 1

if __name__ == "__main__":
    exit(main())