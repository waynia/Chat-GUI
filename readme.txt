Readme | [简体中文]()

This tool is a GUI interface implemented for dialog using Flask. Although it has not yet integrated the OpenAI knowledge base query function, it already has all the necessary foundations. The GUI interface can achieve the following effects:

1. When opening the interface for the first time, users need to enter their OpenAI API Key. The program will save it in the Cookie and provide a way for users to delete the Key. The program will call OpenAI's function to verify the validity of the API Key, ensuring that the Key is usable.

2. With a valid API Key, the epub file upload button will be visible. Users can click the button or drag and drop an epub file into the GUI interface, and the program will upload the file to the "uploads" folder. Then, it will generate a CSV file with the same name as the uploaded file in the backend. The function to generate the CSV file is parse_book, which has no specific execution code in its body. The next step is to call the function to analyze the epub file and generate embeddings within it.

3. The program will check if there are any CSV files in the "uploads" folder. If there are, the chat dialogue box will become visible. Users can enter any text in the input box, and the program will call the process_input function in the backend to traverse all CSV files in the "uploads" folder and then analyze the input text. There is no specific execution code for the analysis part; the next step is to call the function to calculate the embedding of the user's input and retrieve the record with the highest similarity value from the CSV.

4. The program has not yet implemented the retention of user conversations and memory functionality.