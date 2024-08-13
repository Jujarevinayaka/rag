# Generative AI-Based Feedback Response System with Backend Integration
## Objective
Develop a generative AI-based system that generates automated responses to customer
feedback. The system should include both AI/ML components for generating responses and
backend integration for handling data storage and API interactions.

Please refer the following for more details
- [Detailed Requirements](#detailed-requirements)
- [Approach](#approach)


## Architecture
### Overview
- The chatbot system is designed to process customer feedback and provide relevant responses using a custom-built language model.
- The system consists of a front-end interface and a back-end application that integrates with a Retrieval-Augmented Generation (RAG) model for generating responses.
![alt text](https://github.com/Jujarevinayaka/rag/blob/main/imgs/Arch.png)

### Front-End Interface
- **HTML Interface**
    - A HTML user-friendly web interface is built using Flask.
    - This interface allows users to interact with the chatbot by submitting feedback and receiving responses through a simple chat window.
- **Functionalities**
    - POST /generate-response: Users can submit customer feedback through this endpoint, and the application returns a generated response.
    - GET /metrics: This endpoint allows users to retrieve performance metrics (BLEU score) of the generative model.
### Back-End System
- **Application Logic**
    - The Flask application handles user requests, interacts with the LLM to generate responses, and respond back to the user with the generated response.
    - The application also stores the user feedback and the generated responses in a file.
- **Language Model**
    - The model is a custom LLM created using Ollama and LLaMA 3.1, enhanced with RAG for generating accurate responses.
    - The model is fine-tuned using input samples of feedback-response pairs and publicly available data on Ctruh to ensure relevant and context-aware responses.
- **Performance Evaluation**
    - The chatbot's performance is evaluated using the BLEU score, which measures the accuracy and relevance of the generated responses compared to reference responses.
    - The BLEU score is accessible via the GET /metrics endpoint.
### Data Storage
- **Conversation History**
    - User interactions and generated responses are stored in a file, acting as a simple database for future reference or analysis.
    - This also includes the amount of time it took for the LLM to generate a response for the given input.
- **Metrics**
    - Model evaluation metrics (BLEU score) for a standard set of input feedback are stored in a file, to help in comparing and evaluating the performance of a new model.
    - The mean value of all these individual BLEU scores is the overall BLEU score of the model.
- **LLM and Vector Database**
    - The LLM (LLaMA 3.1) and the vector database are stored locally.
    - The vector database (which is trained with additional data) is used to efficiently retrieve relevant contextual information during the generation of responses.

## Usage
### Setup
- Download and install [Ollama](https://ollama.com/download) - used in downloading LLMs locally.
- Clone the repository - `git clone https://github.com/Jujarevinayaka/rag.git`
- Change directory - `cd rag`
- [Update the env variable](https://skillsfoster.com/change-model-save-location-for-ollama-on-windows/) `OLLAMA_MODELS` with the full path of `models/` folder present in the cloned repository.
- Run `ollama pull llama3.1` to download [llama3.1](https://ollama.com/library/llama3.1) model from Ollama into the `models/` folder in the cloned repository.

### Execution
#### **Native Windows**
- Run `python App.py` to initiate the app.
- Open `http://localhost:5000/` to see the landing page for the c-bot
![alt text](https://github.com/Jujarevinayaka/rag/blob/main/imgs/c-bot_landing_page.PNG)

#### **Using Docker image**
- Create the docker image - `docker build -t cllama:0.1 .`
- Run the image while mounting current directory - `docker run -p 5000:5000 -d -v <current directory where the repository is cloned>/:/app cllama:0.1`
- Open `http://127.0.0.1:5000/` to see the landing page for the c-bot
![alt text](https://github.com/Jujarevinayaka/rag/blob/main/imgs/c-bot_landing_page.PNG)

#### **Examples of feedback and response**
- Based on the testing, the response times vary depending on the resource availability for the app
    - On windows with RTX360-TI GPU, the response can come within 5-15sec
    - While using docker without a GPU availability, the response can come within 5-60sec
- The conversation history is stored under `history/conversations_df.tsv`
- User can either use the UI or requests model to send the feedback or get metrics.
    ##### **Using the UI**
    - The user can input feedback via the landing page chat UI
    - To get metrics, the user can use the **'Get Metrics'** button, which currently returns the BLEU score.
    ![alt text](https://github.com/Jujarevinayaka/rag/blob/main/imgs/c-bot_conversation.PNG)

    ##### **Using requests module**
    - Use requests module to interact with the app.
    - POST feedback to the custom LLM.
    ```
    import requests

    url = 'http://localhost:5000/generate-response'
    myobj = {'feedback': 'The UI is extremely intuitive.'}
    x = requests.post(url, json = myobj)
    print(x.text)
    ```
    - GET the evaluation metrics
    ```
    import requests

    url = 'http://localhost:5000/metrics'
    x = requests.get(url)
    print(x.text)
    ```


## Detailed Requirements:
- ### Problem Definition
    Business Use Case: Develop a system that generates automated responses to customer feedback using a generative AI model.
- ### AI/ML Model Development
    - **Dataset**: Use a publicly available dataset or create a small dataset of customer feedback and corresponding responses.
    - **Preprocessing**: Clean and preprocess the data (e.g., tokenization).
    - **Model Training**: Use a pre-trained language model (e.g., GPT-3, GPT-2, or any other suitable model) and fine-tune it on the feedback-response dataset.
    - **Evaluation**: Evaluate the model using metrics like BLEU score or human evaluation for response quality.
- ### Backend Development
    - **API Development**: Develop RESTful APIs using a framework of your choice (e.g., Flask, Express.js) with the following endpoints:
        - POST /generate-response: Accepts customer feedback and returns the generated response.
        - GET /metrics: Returns the performance metrics of the generative model.
    - **Data Storage**: Implement basic storage (in-memory or a simple database) to store feedback, generated responses, and evaluation metrics.
- ### System Integration
    - **Integration Testing**: Ensure that the generative AI model and the backend work together seamlessly.
- ### Documentation
    - **Technical Documentation**: Provide a brief document outlining the architecture, design decisions, and how to run the system.
- ### Deliverables:
    - **Source Code**: Well-documented source code for the generative AI model and backend.
    - **Documentation**: A brief document explaining the architecture and usage.
- ### Evaluation Criteria:
    - **Technical Accuracy**: Quality and coherence of the generated responses.
    - **Integration**: Seamless integration between the generative AI model and the backend.
    - **Documentation**: Clarity and completeness of the documentation.
    - **Scalability Considerations**: Basic consideration for how the solution could be scaled or improved in the future.

## Approach
- Considering the **Requirements** and the **Evaluation Criteria**, instead of fine-tuning an open-source LLM, it is better if we use [RAGs](https://aws.amazon.com/what-is/retrieval-augmented-generation/).
- Here are some of the references talking about the differences between fine-tuning and RAG, and also which approach is appropriate for what usecase.
    - [RAG vs. Fine-Tuning: Which Method is Best for Large Language Models (LLMs)?](https://blog.runpod.io/rag-vs-fine-tuning-which-method-is-best-for-large-language-models-llms/#:~:text=However%2C%20RAG%20generally%20outperforms%20fine,in%20about%2075%25%20of%20cases.)
    - [Fine-tuning versus RAG in Generative AI Applications Architecture](https://harsha-srivatsa.medium.com/fine-tuning-versus-rag-in-generative-ai-applications-architecture-d54ca6d2acb8)
    - [When to Apply RAG vs Fine-Tuning](https://medium.com/@bijit211987/when-to-apply-rag-vs-fine-tuning-90a34e7d6d25)
    - [RAG vs Fine Tuning: How to Choose the Right Method](https://www.montecarlodata.com/blog-rag-vs-fine-tuning/#:~:text=What%20is%20the%20difference%20between%20rag%2C%20fine%2Dtuning%2C%20and,improve%20performance%20on%20specific%20tasks.)
- **RAG** enhances an LLM's knowledge by fetching external information during inference, ensuring responses are current and contextually accurate.
- **Fine-tuning** involves retraining an existing LLM on a specific dataset, embedding specialized knowledge directly into the model.
- I have detailed down the [advantages and disadvantages](#rag-vs-fine-tuning) for each of the technique and how RAG is more applicable for our usecase.
### Conclusion
RAG is generally a better approach for developing a feedback response system in this scenario. It combines the strengths of retrieval and generation, providing contextually accurate and relevant responses with less reliance on large fine-tuning datasets. It also offers better scalability and flexibility, which are crucial for handling diverse and dynamic customer feedback.


## RAG v/s fine-tuning
### Advantages and Disadvantages
- **Retrieval-Augmented Generation (RAG)**:
    - **Advantages**:
        - **Contextual Accuracy**: Retrieves relevant information from a knowledge base, which can lead to more accurate and contextually appropriate responses.
        - **Less Data Requirement**: Can perform well with less fine-tuning data since it relies on a combination of retrieval and generation
        - **Scalability**: Easier to update and maintain since the knowledge base can be expanded without re-training the model.
    - **Disadvantages**:
        - **Complexity**: Requires setting up and maintaining a retrieval system along with the generative model.
        - **Latency**: The retrieval process can introduce additional latency.
        - **Integration**: Needs careful integration of the retrieval and generation components.
- **Fine-Tuning**:
    - **Advantages**:
        - **Custom Responses**: The model learns specific patterns and nuances from your dataset, leading to more tailored responses.
        - **Simplicity**: Once fine-tuned, the model can directly generate responses without needing additional components or infrastructure.
        - **Performance**: For specific tasks, fine-tuned models can outperform general models.
    - **Disadvantages**:
        - **Data Requirement**: Requires a large, high-quality dataset to achieve good performance.
        - **Compute Intensive**: Fine-tuning large models can be computationally expensive and time-consuming.
        - **Overfitting**: The model might overfit to the fine-tuning data, leading to less generalizable responses.

### Comparision
- **Quality and Coherence of Responses**:
    - **Fine-Tuning**: Produces responses that are coherent and contextually relevant if the dataset is comprehensive and well-structured.
    - **RAG**: Can provide highly accurate and contextually relevant responses by leveraging the knowledge base, especially useful for diverse and dynamic feedback.
- **Integration**:
    - **Fine-Tuning**: Simpler integration since it involves only one component (the fine-tuned model).
    - **RAG**: More complex integration as it involves both retrieval and generative components.
- **Data Requirements**:
    - **Fine-Tuning**: Requires a large dataset of feedback-response pairs for effective training.
    - **RAG**: Can work with less fine-tuning data by leveraging external knowledge sources.
- **Scalability**:
    - **Fine-Tuning**: Scaling requires retraining the model with new data, which can be time-consuming and resource-intensive.
    - **RAG**: Easier to scale by simply updating the knowledge base.
- **Performance Metrics**:
    - **Fine-Tuning**: Performance depends heavily on the quality and size of the fine-tuning dataset.
    - **RAG**: Can achieve good performance with a smaller fine-tuning dataset due to the retrieval mechanism.