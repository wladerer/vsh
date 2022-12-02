package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

func main() {
	// Check if the path to the file is provided as an argument
	if len(os.Args) < 2 {
		fmt.Println("Usage: converged <path_to_file>")
		os.Exit(1)
	}

	// Get the path to the file from the command-line argument
	path := os.Args[1]

	// Check if the file contains the string "reached required accuracy"
	b, err := ioutil.ReadFile(path)
	if err != nil {
		fmt.Println("Error: unable to read file")
		os.Exit(1)
	}
	if strings.Contains(string(b), "reached required accuracy") {
		fmt.Println("Converged")
	} else {
		fmt.Println("Convergence not reached")
	}
}