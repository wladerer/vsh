package main

import (
    "bufio"
    "fmt"
    "os"
    "path/filepath"
    "strings"
)

func main() {
    // Open the input PDB file
    pdbFile, err := os.Open(os.Args[1])
    if err != nil {
        panic(err)
    }
    defer pdbFile.Close()

    // Get the base name of the input PDB file
    pdbBase := filepath.Base("input.pdb")

    // Create a new text file for the PDB header
    headerFile, err := os.Create(fmt.Sprintf("%s_PDB_header.txt", strings.TrimSuffix(pdbBase, filepath.Ext(pdbBase))))
    if err != nil {
        panic(err)
    }
    defer headerFile.Close()

    // Read the PDB file line by line
    scanner := bufio.NewScanner(pdbFile)
    for scanner.Scan() {
        // Trim leading and trailing whitespace from the line
        line := strings.TrimSpace(scanner.Text())

        // Stop reading when we reach the first ATOM
        if strings.HasPrefix(line, "ATOM") {
            break
        }

        // Write the line to the header file
        fmt.Fprintln(headerFile, line)
    }
}
