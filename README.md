# Chromagraphic

Chromagraphic is a powerful tool that allows you to control and view ChromaDB collections and their documents using a user-friendly graphical user interface (GUI). With Chromagraphic, you can easily manage your collections, add new documents, and perform various operations on your data.
This tool was something I made while in the process of developing a project that required adding lots of data into a vector database. I wanted an intuitive and easy way to add the data without having to run in a python notebook, and am excited to be able to share it with the world!

Chromagraphic was devloped using Python and Javascript

## Walkthrough

Main Page:
You can select your collection with the dropdown, or add a new collection. Additionally, you can view all of the documents in the currently selected collection by clicking the dropdown by the documents. The document view window shows the source metadata and the text content in that document.
<img width="1512" alt="Screenshot 2023-06-10 at 2 25 57 PM" src="https://github.com/msteele3/chromagraphic/assets/94016758/857905e8-c645-4f28-b888-e1839a289980">

Add Document Page:
On the document adding page, you can add the document information in the fields and select which collection to add it to.
<img width="1512" alt="Screenshot 2023-06-10 at 2 26 03 PM" src="https://github.com/msteele3/chromagraphic/assets/94016758/7b7f5fd0-13ab-4c6f-a663-60e724c11578">

## Getting Started

To use Chromagraphic, follow the instructions below:

1. Clone the repository to your local machine.
2. Navigate to the root folder of the project.
3. Make sure you have Python installed (version 3.7 or above).
4. Install the required dependencies by running the following command:
5. Launch the program by running the following command in the terminal:
   ```
   python main.py
   ```

## Features

- **Collection and Document Management**: Easily select and manage your ChromaDB collections and documents through an intuitive dropdown interface.
- **Add New Collections**: Quickly create new collections directly from the main page.
- **Add Documents**: Seamlessly add new documents to your ChromaDB collection by navigating to the "Add Document" page.
- **User-Friendly Interface**: Enjoy a visually appealing and easy-to-use GUI for efficient data management.

## Libraries Used

Chromagraphic is built with the help of the following libraries:

- [Eel](https://github.com/python-eel/Eel): A little Python library for making simple Electron-like HTML/JS GUI apps
- [ChromaDB](https://github.com/example/chromadb): An open source vector database, using it being the focus of this project.
- [OpenAI](https://openai.com/): OpenAI's embedding model is used to embed data into this version of ChromaGraphic.

## Contributing
Any input on features is welcome.

## Future Features

A search page is currently being developed in order to simulate the queries one might make inside of an application to allow for testing the inputted data. Additionally, selection of embedding function will become an available GUI function in the near future.


## Contact

For any questions or inquiries, please contact me at mpsteele553@gmail.com


Regards,


Matt
