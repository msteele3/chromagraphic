
window.addEventListener('DOMContentLoaded', (event) => {
  console.log("LOADED ADD DOC")
  updateCollectionsDropdown();

  const collectionSelect = document.getElementById('collection-select');
  if (collectionSelect) {
    collectionSelect.addEventListener('change', () => {
      updateCollectionsDropdown();
      console.log("Document dropdown changed");
    });
  }
});


function goHome() {
  window.location.href = './index.html';
}

function updateCollectionsDropdown() {
  const selectElement = document.getElementById('collection-select');
  let collectionList = [];
  const promised = eel.get_collections_list()().then((result) => {
    let collectionList = result;
    if (collectionList.length === 0) {
      const defaultOption = document.createElement('option');
      defaultOption.text = 'No collections made yet';
      selectElement.appendChild(defaultOption);
    } else {
      for (const collection of collectionList) {
        const option = document.createElement('option');
        option.text = collection;
        option.value = collection;
        selectElement.appendChild(option);
      }
    }
  });
  selectElement.innerHTML = '';
}


function submitNewDocument() {
  var collectionName = document.getElementById("collection-select").value;
  var documentName = document.getElementById("document-name").value;
  var documentSource = document.getElementById("document-source").value;
  var documentContent = document.getElementById("document-content").value;

  var validForm = validateForm();
  if (!validForm) {
    return
  }
  console.log("Collection Name: ", collectionName);
  console.log("Document Name: ", documentName);
  console.log("Document Source Url: ", documentSource);
  console.log("Document Content: ", documentContent);
  eel.add_document(collectionName, documentName, documentSource, documentContent);
  //    add_document_to_collection(current_collection, document_name, document_contents, document_source, id=(current_collection.count()+1))
  setTimeout(goHome(), 500);
  // Add your desired functionality here
}

function validateForm() {
  var collectionName = document.getElementById("collection-select").value;
  var documentName = document.getElementById("document-name").value;
  var documentSource = document.getElementById("document-source").value;
  var documentContent = document.getElementById("document-content").value;

  var collectionNameRegex = /^(?!.*\.\.)(?!.*\.$)(?!^[0-9.]*$)(?!^.*(\.\d{1,3}){4}$)[a-z0-9][a-z0-9._-]{3,}[a-z0-9]$/;
  var documentNameRegex = /^[a-zA-Z0-9]+$/;
  var urlRegex = /^(https?|http):\/\/[^\s/$.?#].[^\s]*$/;

  if (!collectionName || !collectionNameRegex.test(collectionName)) {
    alert("Invalid collection name!");
    return false;
  }

  if (!documentName || !documentNameRegex.test(documentName)) {
    alert("Invalid document name! Only lowercase or uppercase letters and numbers are allowed.");
    return false;
  }

  if (!urlRegex.test(documentSource)) {
    alert("Invalid document source! Please enter a valid URL starting with 'https://' or 'http://'.");
    return false;
  }

  if (documentContent.trim() === "") {
    alert("Please enter the document content!");
    return false;
  }
  return true;
}
