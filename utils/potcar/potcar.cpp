#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

void potcar(const std::string& file) {
    std::ifstream inputFile(file);
    if (!inputFile.is_open()) {
        std::cerr << "Failed to open file: " << file << std::endl;
        return;
    }

    std::string line;
    for (int i = 0; i < 6; i++) {
        std::getline(inputFile, line);
    }

    std::vector<std::string> symbols;
    std::istringstream iss(line);
    std::string symbol;
    
    while (iss >> symbol) {
        symbols.push_back(symbol);
    }

    for (const auto& symbol : symbols) {
        std::ifstream potentialFile("Potentials/" + symbol + "/POTCAR");
        if (!potentialFile.is_open()) {
            std::cerr << "Failed to open POTCAR file for symbol: " << symbol << std::endl;
            continue;
        }

        std::string potentialLine;
        while (std::getline(potentialFile, potentialLine)) {
            std::cout << potentialLine << std::endl;
        }

        potentialFile.close();
    }

    inputFile.close();
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "Usage: potcar <POSCAR file>" << std::endl;
        return 1;
    }

    potcar(argv[1]);

    return 0;
}
