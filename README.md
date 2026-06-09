# Agente n8n para classificação de solicitações de compra em SAP

Esse agente automatiza o processo de leitura, pré-processamento e classificação de solicitações de compras via email, simulando um ambiente corporativo com o sistema ERP SAP.

## Inicialização do projeto

`cd python_service`

`pip install -r requirements.txt -r requirements-dev.txt`

`docker compose build --no-cache`

`docker compose up -d`

Abrir url do cloudflare para acessar n8n.

# Fluxo do agente

![Email Trigger IMAP](./docs/images/image.png)

**Nó Email Trigger IMAP**: Lê emails recebidos e inicializa a automação

**Nó Email parser**: Captura assunto, email de quem solicitou e corpo do email.

![Email parser](./docs/images/image-1.png)

**Nó If has attachments**: Verifica se o email tem anexos: se sim, lê anexo.

![If has attachments](./docs/images/image-2.png)

**Nó Get attachments**: Captura os binários do email (anexos)

![Get attachments](./docs/images/image-3.png)

**Nó LLM Request Builder**: Combina as duas opções (email com anexo e email sem anexo) e monta um JSON estruturado

![LLM Request Builder](./docs/images/image-4.png)

![2 parte do fluxo](./docs/images/image-5.png)

**Nó HTTP Request**: POST /python:8080/emailProcessingService, realiza pré-processamento do email:

* Route /emailProcessingService

  **Helpers:**

* Function **process_email_batch**
* Function **_process_single_email**
* Function **_extract_email_address**
* Function **_clean_subject**
* Function **remove_email_footer**
* Function **_process_attachments**
* Function **_build_attachment_preview**: Retorna primeiros 5000 bytes do anexo para resumo
* Function **_decobe_base_64**
* Function **_extract_pdf_preview**

![Rota processEmailService](./docs/images/image-6.png)
![Output HTTP Request](./docs/images/image-8.png)

**Contexto SAP e regras para nível de confiança da resposta**: Nó que armazena de forma simples as regras que o Agente deve seguir

![Contexto SAP](./docs/images/image-7.png)
![Regras para nível de certeza da resposta](./docs/images/image-9.png)

**Nó Agente de IA**: Modelo Gemini 3.1-flash-lite

![Agente de IA](./docs/images/image-10.png)

**Structured output parser**: Nó que itera pelo modelo de LLM para estruturar resposta de acordo com as regras

![Structured Output Parser](./docs/images/image-11.png)

![3 parte do fluxo](./docs/images/image-12.png)

**Nó Switch**: Com base no nível de certeza, esse switch redireciona o fluxo para as melhores ações no momento: responder email pedindo mais informações, pedindo confirmação e aprovação ou enviando o ouput para a API do SAP, para processamento da solicitação de compra.

![Switch node](./docs/images/image-13.png)

**Nó Send Email**: Com base no roteamento do switch, o fluxo envia um email para o remetente original pedindo mais informações para completar a classificação.

![Email sent](./docs/images/image-14.png)
![Email received](./docs/images/image-15.png)