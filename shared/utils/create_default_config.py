#!/usr/bin/env python3
"""
Script para criar configuração padrão quando não existe
"""

import sys
import os
from validation_config_builder import ValidationTemplates

def main():
    if len(sys.argv) != 4:
        print("Uso: python create_default_config.py <config_path> <course> <module>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    course = sys.argv[2]
    module = sys.argv[3]
    
    try:
        # Criar configuração usando template
        config = ValidationTemplates.web_application_template()
        config.config['name'] = f'Validação {course} - {module}'
        config.config['description'] = f'Configuração padrão para {course}/{module}'
        
        # Salvar arquivo
        config.save_to_file(config_path)
        print(f'✅ Configuração padrão criada em: {config_path}')
        
    except Exception as e:
        print(f'❌ Erro ao criar configuração padrão: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()
