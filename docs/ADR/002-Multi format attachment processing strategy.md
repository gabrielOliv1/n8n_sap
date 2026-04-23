28-03-2026 19:26

Status: Building

Tags: [[Purchase AI Classifier]]

ID: 002



# Multi format attachment processing strategy

# 1. Business context

The automation needs to process emails with possible many attachments in different formats (PDF, XLSX, DOCX, etc). The goal is to extract general context from the email along with the attachment data to request an analysis by a LLM Model. The challenge is to keep track of email context, respective attachments and the variety of file formats.

# 2. Limitations

1. n8n's functionality to deal with multiple files and to send multipart/form-data in a single requisition is poor;
2. Process attachments individually, by Split out functionality, would increase complexity to handle multiple attachments in an API call;
3. Send base64 directly to LLM Model would increase costs.

# 3. Technical decision: Pre-processing base64 JSON payload

Considering the limitations above, it is recommended to process a single JSON containing email general data (sender, subject and body) plus the attachment as base64, decoding it in using a Python API.

# 4. Trade-offs

***PROS***
- Context intregity: API will receive all the necessary context under a single requisition;
- Low technical barrier: avoid handling n8n complexity to manage multiple binary data;
- Cost reduction: using a Middleware API with a Python code will reduce costs by cleaning "trash data" and providing LLM model only necessary data to perform analysis;
- Extensibility: Allows to add easily logic to parse file
***CONS***
- Overhead: base64 increase payload size up to ~33%;
- RAM Usage: in the worst case, while processing a 25MB attachment (probably never), the  API will require RAM usage peaks up to 100MB;
- Network latency: Higher upload time due to bigger payload.

# 5. Cost and performance analysis

| METRIC             | ESTIMATED IMPACT         | OBSERVATION                                                |
| ------------------ | ------------------------ | ---------------------------------------------------------- |
| Network traffic    | +33% volum               | Irrelevant, considering it will handle files with >= 25 mb |
| LLM API costs      | Reduction between 70-90% | Sending clean data instead of complete payload             |
| Processing latency | +200-500ms               | encoding/decoding base64                                   |
| Infra costs (API)  | Low                      | RAM escalability is a plus                                 |

# 6. Alternatives

- Multipart/form-data: within n8n: complex to handle dynamic emails and their attachments arrays.
- Parsing within n8n: limitations to set up multiple formats processing 

# 7. JSON Payload

The payload received from n8n will follow a dictionary structure able to process 0:N files in one requisition.

***PAYLOAD EXAMPLE***

{
  "email": email_1774740308832 ,
  "requisitioner": "usuario@empresa.com.br",
  "subject": "Relatórios Mensais de Vendas",
  "body": "Seguem os arquivos em PDF e a planilha de conferência.",
  "attachment_data": {
    "attachment_0": {
      "mimeType": "application/pdf",
      "fileType": "pdf, 
      "fileExtension": "pdf",
      "data": "asaasasada...",
      "fileName": "contract.pdf",
      "fileSize": "40.kb"
    },
    "attachment_1": {
      "mimeType": "application/pdf",
      "fileType": "pdf, 
      "fileExtension": "pdf",
      "data": "asaasasada...",
      "fileName": "contract2.pdf",
      "fileSize": "40.kb"
    }
  },
  {
   "email": email_1774740308833 ,
  "requisitioner": "usuario1@empresa.com.br",
  "subject": "Relatórios Mensais",
  "body": "Seguem os arquivos em PDF e a planilha de conferência.",
  "attachment": undefined
  }
}

- attachment: can be filled or to be undefined
****
# References