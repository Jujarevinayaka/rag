##########################################################################################
##                          Test - End to End  and unit testing                         ##
##                                                                                      ##
##  Description: This contains all the testcases for end to end and unit testing.       ##
##  Author: Vinayaka Jujare                                                             ##
##  Usage:                                                                              ##
##      Tests: py.test -s ./Test.py                                                     ##
##      Coverage: coverage run --source=./ -m pytest -v ./Test.py && coverage report -m ##
##########################################################################################

import json
import pytest
from App import app
from Create import DOCUMENTS, VECTORDB
from unittest.mock import patch, mock_open, MagicMock


@pytest.fixture(scope='function')
def client():
    """
    Configures and initiates the app for testing.

    @return: App for testing
    """
    app.testing = True
    yield app.test_client()

@pytest.fixture(scope='function')
def mock_llm(monkeypatch):
    """
    Patch the LLM object to return a mock response.
    """
    class MockLLM:
        def chat(self, feedback):
            return "Mock response from LLM"

    monkeypatch.setattr('App.llm', MockLLM())

@pytest.fixture(scope='function')
def documents():
    return DOCUMENTS()

@pytest.fixture(scope='function')
def vectordb(documents):
    return VECTORDB(main_doc_dir=documents.main_doc_dir)


# --------------------------------- Test App related functions --------------------------------- #
def test_landing_page(client):
    """
    Test the landing page of the app.
    """
    response = client.get(
        "/",
        content_type='application/json'
    )
    response_status = response.status_code
    response_text = response.text
    request_url = response.request.url

    assert response_status == 200
    assert request_url == 'http://localhost/'
    assert response_text == "POST 'generate-response' to give feedback and get appropriate response! GET 'metrics' tog get the Evaluation metrics."

def test_generate_response_valid(client):
    """
    Test for a valid POST request with valid feedback.
    """
    # Valid POST request with feedback
    feedback_data = {'feedback': 'The product is amazing!'}
    response = client.post(
        '/generate-response',
        data=json.dumps(feedback_data),
        content_type='application/json'
    )
    response_status = response.status_code
    response_data = json.loads(response.data)
    request_url = response.request.url

    assert response_status == 200
    assert request_url == 'http://localhost/generate-response'
    assert 'response' in response_data
    assert response_data['response'] != ''

def test_generate_response_empty_feedback(client):
    """
    Test for a valid POST request with empty feedback.
    """
    # Empty feedback
    feedback_data = {'feedback': ''}
    response = client.post(
        '/generate-response',
        data=json.dumps(feedback_data),
        content_type='application/json'
    )
    response_status = response.status_code
    response_data = json.loads(response.data)
    request_url = response.request.url

    assert response_status == 200
    assert request_url == 'http://localhost/generate-response'
    assert 'response' in response_data
    assert response_data['response'] != ''

def test_generate_response_long_feedback(client):
    """
    Test for a valid POST request with a long feedback.
    """
    # Extremely long feedback
    feedback_data = {'feedback': 'a' * 10000}
    response = client.post(
        '/generate-response',
        data=json.dumps(feedback_data),
        content_type='application/json'
    )
    response_status = response.status_code
    response_data = json.loads(response.data)
    request_url = response.request.url

    assert response_status == 200
    assert request_url == 'http://localhost/generate-response'
    assert 'response' in response_data
    assert response_data['response'] != ''

def test_generate_response_invalid_format(client):
    """
    Test for a invalid POST request due to invalid format.
    """
    # Invalid POST request (not a dictionary)
    feedback_data = ['Invalid feedback']
    response = client.post(
        '/generate-response',
        data=json.dumps(feedback_data),
        content_type='application/json'
    )
    response_status = response.status_code
    response_text = response.text
    request_url = response.request.url

    assert response_status == 400
    assert request_url == 'http://localhost/generate-response'
    assert response_text == "Invalid POST request, should be in the format of {'feedback': 'some feedback'}"

def test_generate_response_missing_feedback_key(client):
    """
    Test for a invalid POST request due to invalid format.
    """
    # Invalid POST request (missing feedback key)
    feedback_data = {'comment': 'The product is amazing!'}
    response = client.post(
        '/generate-response',
        data=json.dumps(feedback_data),
        content_type='application/json'
    )
    response_status = response.status_code
    response_text = response.text
    request_url = response.request.url

    assert response_status == 400
    assert request_url == 'http://localhost/generate-response'
    assert response_text == "Invalid POST request, should be in the format of {'feedback': 'some feedback'}"

def test_generate_response_invalid_content_type(client):
    """
    Test for a invalid POST request due to invalid content type.
    """
    # POST request with non-JSON content type
    feedback_data = 'feedback=The product is amazing!'
    response = client.post(
        '/generate-response',
        data=feedback_data,
        content_type='application/x-www-form-urlencoded'
    )
    response_status = response.status_code
    response_text = response.text
    request_url = response.request.url

    assert response_status == 415
    assert request_url == 'http://localhost/generate-response'
    assert "Unsupported Media Type" in response_text

def test_generate_response_malformed_json(client):
    """
    Test for a invalid POST request due to malformed data.
    """
    # POST request with malformed JSON
    feedback_data = '{"feedback": "The product is amazing!"'
    response = client.post(
        '/generate-response',
        data=feedback_data,
        content_type='application/json'
    )
    response_status = response.status_code
    response_text = response.text
    request_url = response.request.url

    assert response_status == 400
    assert request_url == 'http://localhost/generate-response'
    assert 'Bad Request' in response_text

def test_metrics(client):
    """
    Test for a GET request for metrics.
    """
    # Test the metrics GET request
    response = client.get('/metrics')
    response_status = response.status_code
    response_data = json.loads(response.data)
    request_url = response.request.url

    assert response_status == 200
    assert request_url == 'http://localhost/metrics'
    assert response_data == {"BLEU score": 0.85}

def test_generate_response_mock_llm(client, mock_llm):
    """
    Test for a valid POST request with mocked LLM response.
    """
    # Use the mocked LLM object
    feedback_data = {'feedback': 'Test feedback'}
    response = client.post(
        '/generate-response',
        data=json.dumps(feedback_data),
        content_type='application/json'
    )
    response_status = response.status_code
    response_data = json.loads(response.data)
    request_url = response.request.url

    assert response_status == 200
    assert request_url == 'http://localhost/generate-response'
    assert 'response' in response_data
    assert response_data['response'] == 'Mock response from LLM'

# ------------------------------- Test Create related functions ------------------------------- #
@patch("Create.webdriver.Edge")
@patch("Create.EdgeChromiumDriverManager")
@patch("Create.Options")
def test_get_docs_from_web(mock_options, mock_driver_manager, mock_edge, documents):
    """
    Test the function __get_docs_from_web.
    """
    mock_driver = MagicMock()
    mock_edge.return_value = mock_driver
    # Set the content of the web page
    mock_driver.find_element.return_value.text = "Header\n\n\n\nContent of the page"

    url = "http://example.com"
    content = documents._DOCUMENTS__get_docs_from_web(url)

    mock_driver.get.assert_called_once_with(url)
    assert content == "Content of the page"

@patch("Create.open", new_callable=mock_open)
def test_feedback_doc(mock_open, documents):
    """
    Test the function _feedback_doc.
    """
    documents._feedback_doc()
    mock_open.assert_called_once_with(documents.custom_feedback_doc, 'w')
    handle = mock_open()
    # Ensure data is written to the file
    handle.write.assert_called()

@patch("Create.webdriver.Edge")
@patch("Create.EdgeChromiumDriverManager")
@patch("Create.Options")
@patch("Create.open", new_callable=mock_open)
def test_url_docs(mock_open, mock_options, mock_driver_manager, mock_edge, documents):
    """
    Test the url parsing function.
    """
    mock_driver = MagicMock()
    mock_edge.return_value = mock_driver
    mock_driver.find_element.return_value.text = "Header\n\n\n\nContent of the page"

    documents._url_docs()

    # Ensuring 35 URLs are processed
    assert mock_open.call_count == 35
    # Ensuring that the URLs were accessed
    mock_driver.get.assert_called()

@patch("Create.DirectoryLoader")
@patch("Create.OllamaEmbeddings")
@patch("Create.RecursiveCharacterTextSplitter")
@patch("Create.Chroma.from_documents")
def test_create_vector_db(mock_chroma, mock_text_splitter, mock_embeddings, mock_loader, vectordb):
    """
    Test the vector db creation function.
    """
    mock_documents = MagicMock()
    mock_loader.return_value.load.return_value = mock_documents
    mock_texts = MagicMock()
    mock_text_splitter.return_value.split_documents.return_value = mock_texts

    vectordb.create_vector_db()

    mock_loader.return_value.load.assert_called_once()
    mock_text_splitter.return_value.split_documents.assert_called_once_with(mock_documents)
    mock_chroma.assert_called_once_with(documents=mock_texts, embedding=mock_embeddings.return_value, persist_directory=vectordb.db_dir)

def test_create_documents(documents):
    """
    Test create_documents function.
    """
    with patch.object(documents, '_url_docs') as mock_url_docs, \
         patch.object(documents, '_feedback_doc') as mock_feedback_doc:
        documents.create_documents()

        mock_url_docs.assert_called_once()
        mock_feedback_doc.assert_called_once()
