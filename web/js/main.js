var defaultPath = '/chroma_database';
var defaultCollectionName = "collection1";

window.addEventListener('DOMContentLoaded', (event) => {
    
    const pathInputContainer = document.querySelector('.path-input-container');
    const addCollectionContainer = document.querySelector('.add-collection-div');
    const changePathBtn = document.querySelector('.change-path-btn');
    const submitPathBtn = document.querySelector('.submit-path-btn');
    const createCollectionButton = document.querySelector('.create-collection-button');
    const submitCollectionButton = document.querySelector(".submit-new-collection");
    const deleteCollectionButton = document.querySelector(".delete-collection-button");
    const collectionSelect = document.getElementById('collection-select');
    const deleteDocumentBtn = document.getElementById('delete-document-btn')
    updateCollectionsDropdown();
    updateDocumentsDropdown();

    if(pathInputContainer){
        pathInputContainer.style.display = 'none';
    }  
    if(addCollectionContainer){
        addCollectionContainer.style.display = 'none';
    }
    chromaClientPath = document.getElementById('chroma-client-path');
    if(chromaClientPath){
        chromaClientPath.textContent = defaultPath
    }
    
    if(changePathBtn){
        changePathBtn.addEventListener('click', () => {
            if(pathInputContainer.style.display === 'none'){
                pathInputContainer.style.display = 'block';
            }
            else{
                pathInputContainer.style.display = 'none'
            }
        });
    }
   
    if(submitPathBtn){
        submitPathBtn.addEventListener('click', () => {
            pathInputContainer.style.display = 'none';
            var pathInput = document.getElementById('path-input').value;
            document.getElementById('chroma-client-path').textContent = pathInput;
            let update = eel.remake_client(pathInput)();
            updateCollectionsDropdown()
            console.log(update)
        });
    }
   

    if(createCollectionButton){
        createCollectionButton.addEventListener('click', () => {
            if(addCollectionContainer.style.display === 'none'){
                addCollectionContainer.style.display = 'block';
            }
            else{
                addCollectionContainer.style.display = 'none'
            }
        });
    }

    if(submitCollectionButton){
        submitCollectionButton.addEventListener('click', () => {
            addCollectionContainer.style.display = 'none';
            const collectionNameInput = document.getElementById('collection-name');
            const collectionName = collectionNameInput.value;
            collectionNameInput.value = "";
            eel.add_new_collection(collectionName)();
            updateCollectionsDropdown();
        });
    }

    if(deleteCollectionButton){
        console.log("This loads")
        deleteCollectionButton.addEventListener('click', () => {
            console.log("TEST")
            const selectElement = document.getElementById('collection-select');
            const collectionName = selectElement.value;
            console.log(collectionName);
            eel.remove_collection(collectionName)().then(() => {
                updateCollectionsDropdown();
            });

        });
    }

    if (collectionSelect) {
        collectionSelect.addEventListener('change', () => {
            updateDocumentsDropdown();
            updateDocumentBox()
            console.log("Document dropdown changed");
        });
    }

    if(deleteDocumentBtn){
        console.log("snarty prants")
        deleteDocumentBtn.addEventListener('click', () => {
            console.log("clicked the deleter")
            deleteDocument();
        })
    }
    
});



function goHome() {
    window.location.href = './index.html'; // Replace with your desired URL
  }

  function submitNewDocument() {
    var collectionName = document.getElementById("collection-name").value;
    var documentName = document.getElementById("document-name").value;
    var documentSource = document.getElementById("document-source").value;
    var documentContent = document.getElementById("document-content").value;

    console.log("Collection Name: " + collectionName);
    console.log("Document Name: " + documentName);
    console.log("Document Source: " + documentSource);
    console.log("Document Content: " + documentContent);
    setTimeout(goHome, 2000);
}

function updateCollectionsDropdown() {
    // Run the function that returns the list
    const selectElement = document.getElementById('collection-select');
    let collectionList = [];
    const promised = eel.get_collections_list()().then((result) => {
        let collectionList = result;
        if (collectionList.length === 0) {
            const defaultOption = document.createElement('option');
            defaultOption.text = 'No collections made yet';
            selectElement.appendChild(defaultOption);
          } else {
            // If the collection list is not empty, create options for each item
            for (const collection of collectionList) {
              const option = document.createElement('option');
              option.text = collection;
              selectElement.appendChild(option);
            }
          }
        });
    selectElement.innerHTML = '';    
}
function updateDocumentsDropdown() {
    const documentSelect = document.getElementById('document-select');
    const collectionName = document.getElementById('collection-select').value;
    console.log(collectionName);
    if (!collectionName) {
        while (documentSelect.options.length > 0) {
            documentSelect.remove(0);
        }
        const defaultOption = document.createElement('option');
        defaultOption.text = 'No collection selected yet';
        documentSelect.appendChild(defaultOption);
        return;
    }
    eel.get_document_ids(collectionName)().then((result) => {
        let documentIDList = result;
        // Clear existing options
        documentSelect.innerHTML = '';

        if (documentIDList.length === 0) {
            while (documentSelect.options.length > 0) {
                documentSelect.remove(0);
            }
            const defaultOption = document.createElement('option');
            defaultOption.text = 'No documents made yet';
            documentSelect.appendChild(defaultOption);
        } else {
            
            // If the document list is not empty, create options for each item
            for (const documentID of documentIDList) {
                const option = document.createElement('option');
                option.text = documentID;
                option.value = documentID;
                documentSelect.appendChild(option);
            }
        }
    });
}

function updateDocumentBox() {
    const collectionName = document.getElementById('collection-select').value;
    console.log("Doucment colleciton name")
    console.log(collectionName)
    const documentId = document.getElementById('document-select').value
    console.log(documentId)
    eel.get_collection_document_count(collectionName)().then((docCount) => {
        console.log(docCount)
        if(docCount < 1){
            console.log("NOT ENOUGH TO FILL IT, NO UPDATE");
            const sourceElement = document.getElementById("document-source");
            sourceElement.textContent = "No source";
            const textElement = document.getElementById("document-text");
            textElement.textContent = "Please create a document in this collection";
            return
        } else {
            eel.get_document_info(collectionName, documentId)().then((docinfo) => {
                const info = JSON.parse(docinfo);
                const docSource = info.source;
                console.log(docSource)
                const docContent = info.content
                const sourceElement = document.getElementById("document-source");
                if (sourceElement) {
                    sourceElement.textContent = docSource;
                }
                // Set the document text
                const textElement = document.getElementById("document-text");
                if (textElement) {
                    console.log("done baby")
                    textElement.textContent = docContent
                }
            });
        }

    })
   
}

function deleteDocument(){
    const collectionName = document.getElementById('collection-select').value;
    console.log("Document colleciton name")
    console.log(collectionName)
    const documentId = document.getElementById('document-select').value;
    console.log(documentId)
    eel.delete_document(collectionName,documentId);
    updateDocumentsDropdown();
    updateDocumentBox();
}
  
/**
 * 
 * Code for later
 *  const option = document.createElement('option');
    option.value = collection.id;
    option.textContent = collection.name;
    selectElement.appendChild(option);
 */