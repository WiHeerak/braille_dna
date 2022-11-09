#include <iostream>
#include <cstring>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;

int main()
{
	ifstream file;
	file.open("example.txt", ifstream::in);
	
	string line;
    string word;


	while (getline(file, line))
		cout << line << endl;
	file.close(); //닫기

	stringstream ss(line); 
  
	while (ss>>word) {
		cout << word << endl; 
        cout<< word.length() <<endl;
        const size_t len = word.length() + 1;
        wchar_t wcstring[len];

        swprintf(wcstring, len, L"%s", word.c_str());
        wcout << wcstring[1] << endl;
}

    return 0;
}


 