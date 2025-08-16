# Sistema de Validação Configurável

Este sistema permite configurar validações de entrega de forma declarativa usando arquivos YAML, seguindo o princípio de "Infrastructure as Code".

## Como Funciona

### 1. Arquivo de Configuração (YAML)

Crie um arquivo `validation-config.yml` que define todas as validações:

```yaml
name: "Validação M07 - Sistemas de Informação"
description: "Configuração de validações para entrega do módulo 7"

validations:
  folders:
    - path: "src"
      required: true
      description: "Pasta principal do código fonte"
    
  files:
    - path: "README.md"
      required: true
      description: "Arquivo README principal"
      validations:
        - type: "content_contains"
          value: "# "
          description: "Deve conter pelo menos um título"
        - type: "min_lines"
          value: 10
          description: "Deve ter pelo menos 10 linhas"
  
  api_checks:
    - url: "http://localhost:5000/health"
      required: false
      method: "GET"
      expected_status: 200
      description: "Health check do backend"
  
  custom_scripts:
    - name: "lint_check"
      script: "flake8 src/"
      required: false
      description: "Verificação de qualidade do código"
```

### 2. Tipos de Validação Disponíveis

#### Pastas (`folders`)
- Verifica existência de diretórios
- Configurável como obrigatório ou opcional

#### Arquivos (`files`)
- Verifica existência de arquivos
- Validações de conteúdo:
  - `content_contains`: Verifica se texto específico está presente
  - `min_lines`: Número mínimo de linhas
  - `max_lines`: Número máximo de linhas

#### APIs (`api_checks`)
- Testa endpoints HTTP
- Verifica status codes
- Timeout configurável

#### Scripts Personalizados (`custom_scripts`)
- Executa comandos shell
- Captura saída e código de retorno
- Timeout de segurança

### 3. Builder Programático

Para criar configurações via código:

```python
from shared.utils.validation_config_builder import ValidationConfigBuilder

# Criar configuração
config = ValidationConfigBuilder("Meu Projeto", "Descrição do projeto")

# Adicionar validações
config.add_folder_check("src", required=True) \
      .add_file_check("README.md", required=True, validations=[
          config.add_content_validation("min_lines", 10, "Pelo menos 10 linhas")
      ]) \
      .add_api_check("http://localhost:3000", method="GET") \
      .configure_slack("#entregas", mention_on_failure=True)

# Salvar arquivo
config.save_to_file("config/validation-config.yml")
```

### 4. Templates Predefinidos

```python
from shared.utils.validation_config_builder import ValidationTemplates

# Template para aplicação web
web_config = ValidationTemplates.web_application_template()
web_config.save_to_file("config/web-validation.yml")

# Template para app mobile  
mobile_config = ValidationTemplates.mobile_app_template()
mobile_config.save_to_file("config/mobile-validation.yml")

# Template para Data Science
ds_config = ValidationTemplates.data_science_template()
ds_config.save_to_file("config/ds-validation.yml")
```

## Execução

### Via Workflow GitHub Actions

```yaml
- name: Executar validações
  run: |
    cd ci-cd-templates
    PYTHONPATH=. python cursos/sistemas-informacao/M07/scripts/run_validations.py
```

### Localmente

```bash
cd ci-cd-templates
PYTHONPATH=. python cursos/sistemas-informacao/M07/scripts/run_validations.py
```

### Com Configuração Personalizada

```bash
VALIDATION_CONFIG=minha-config.yml PYTHONPATH=. python cursos/sistemas-informacao/M07/scripts/validation_engine.py
```

## Vantagens

1. **Declarativo**: Define o que validar, não como validar
2. **Reutilizável**: Configurações podem ser compartilhadas entre projetos
3. **Extensível**: Novos tipos de validação podem ser facilmente adicionados
4. **Versionável**: Configurações ficam no Git junto com o código
5. **Interface Friendly**: Pode ser facilmente integrado com interfaces web/CLI

## Próximos Passos

- Interface web para criar configurações visualmente
- Mais tipos de validação (Docker, banco de dados, etc.)
- Relatórios em HTML/PDF
- Integração com mais sistemas de notificação
- Cache de resultados para validações caras
