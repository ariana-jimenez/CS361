/*********************************************************************
** Name: microservice.cpp 
** Description: This service prompts the user to enter their desired
** board size and game mode. User input for board size is written to 
** the file "size.txt" and the game mode to "mode.txt"
*********************************************************************/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::ofstream;
using std::stringstream;

/************************************************************************
Function: validate()
Description: This function validates user input by storing the input 
in an array of characters, and then each character is checked for 
double values, negative numbers, letters, and out of bounds values. If 
an invalid character is detected, the user is reprompted to enter a
correct value.
*************************************************************************/

int validate(string prompt)
{
	int input = 0;          // stores user input
	string str;             // stores user input in string 
	int size;               // stores length of input
	char *characters;	    // pointer to create an array of chars
	bool repeat = true;	    // flag for loop

	while (repeat)
	{
		// Set flag to false to exit the while loop 
		repeat = false;

		// Get user input to string format
		getline(cin, str);
        size = str.length() + 1;
        stringstream num(str);
		num >> input;
		
		// Create an array of characters to store the string 
		characters = new char[size];

		for (int x = 0; x < size; x++)
		{
			characters[x] = str[x];
		}

		/* Read each character in array to check for decimals, letters, and 
		 * out of bounds characters. If any of these is found, set repeat to true
		*/
		for (int x = 0; x < (size - 1); x++)
		{	
			if (characters[x] == '.' || isalpha(characters[x]) || !isdigit(characters[x]))
			{
				repeat = true;
			}
		}

        // If user enters nothing, set repeat flag to true
		if (str.empty())
		{
			repeat = true;
		}

        if (prompt == "size")
        {
	        // If input is between 4 - 10, break from loop to return input
	        if (input >= 4 && input <= 10)
	        {
		        delete [] characters;
                break;
	        }

            // Otherwise input is out of bounds, set repeat flag to true 
            else
            {
                repeat = true;
                cout << "Invalid entry. Enter an integer between 4 and 10: " << endl;
            }
        }

        if (prompt == "mode")
        {
             // If input is either 1 or 2, break from loop to return input
            if (input == 1 || input == 2)
	        {
		        delete [] characters;
                break;
	        }

            // Otherwise input is out of bounds, set repeat flag to true
            else
            {
                repeat = true;
                cout << "Invalid entry. Enter either 1 (for easy mode) or 2 (for hard mode): " << endl;
            }
        }

        delete [] characters;
	} 

    return input;
}


int main()
{
    int size;
    int mode;

    // Prompt user to enter desired size of board
    cout << "Enter your desired board size: " << endl;
    cout << "(Number must be between 4 and 10) " << endl;
    size = validate("size");

    // Write board size to file
    ofstream output1;
    output1.open("size.txt");
    output1 << size << endl;
    output1.close();

    // Prompt user to select game mode
    cout << "Select a game mode: " << endl;
    cout << "1. Easy" << endl;
    cout << "2. Hard" << endl;
    mode = validate("mode");

    // Write game mode to file
    ofstream output2;
    output2.open("mode.txt");
    output2 << mode << endl;
    output2.close();
}