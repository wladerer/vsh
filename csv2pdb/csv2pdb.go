package main

import (
    "encoding/csv"
    "fmt"
    "os"
    "strconv"
)

func main() {
    // Open the input CSV file
    csvFile, err := os.Open(os.Args[1])
    if err != nil {
        panic(err)
    }
    defer csvFile.Close()

    // Create a new PDB file
    pdbFile, err := os.Create("output.pdb")
    if err != nil {
        panic(err)
    }
    defer pdbFile.Close()

    // Read the CSV file as a record
    reader := csv.NewReader(csvFile)
    records, err := reader.ReadAll()
    if err != nil {
        panic(err)
    }

    // Write each record to the PDB file as an ATOM record
    for _, record := range records {
        // Validate the number of fields in the record
        if len(record) != 7 {
            panic(fmt.Errorf("invalid CSV record: %q", record))
        }

        // Parse the atom number and coordinates
        atomNum, err := strconv.Atoi(record[0])
        if err != nil {
            panic(fmt.Errorf("invalid atom number: %q", record[0]))
        }
        x, err := strconv.ParseFloat(record[3], 64)
        if err != nil {
            panic(fmt.Errorf("invalid X coordinate: %q", record[3]))
        }
        y, err := strconv.ParseFloat(record[4], 64)
        if err != nil {
            panic(fmt.Errorf("invalid Y coordinate: %q", record[4]))
        }
        z, err := strconv.ParseFloat(record[5], 64)
        if err != nil {
            panic(fmt.Errorf("invalid Z coordinate: %q", record[5]))
        }

        // Write the validated and parsed fields to the PDB file as an ATOM record
        fmt.Fprintf(pdbFile, "ATOM  %5d %4s %3s %c%4d    %8.3f%8.3f%8.3f%6s%6s\n", atomNum, record[1], record[2], ' ', 0, x, y, z, record[6], "")
    }
}

