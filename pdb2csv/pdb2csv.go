package main

import (
    "bufio"
    "encoding/csv"
    "fmt"
    "os"
    "strconv"
    "strings"
)

func main() {
    // Open the input PDB file
    pdbFile, err := os.Open(os.Args[1])
    if err != nil {
        panic(err)
    }
    defer pdbFile.Close()

    // Create a new CSV writer
    csvFile, err := os.Create("pdb.csv")
    if err != nil {
        panic(err)
    }
    defer csvFile.Close()
    writer := csv.NewWriter(csvFile)

    // Read the PDB file line by line
    scanner := bufio.NewScanner(pdbFile)
    for scanner.Scan() {
        // Split the line into fields
        fields := strings.Fields(scanner.Text())

        // Skip the line if it is not an ATOM or HETATM record
        if fields[0] != "ATOM" && fields[0] != "HETATM" {
            continue
        }

        // Validate the number of fields in the record
        if len(fields) < 9 {
            panic(fmt.Errorf("invalid PDB record: %q", scanner.Text()))
        }

        // Parse the atom number and coordinates
        atomNum, err := strconv.Atoi(fields[1])
        if err != nil {
            panic(fmt.Errorf("invalid atom number: %q", fields[1]))
        }
        x, err := strconv.ParseFloat(fields[6], 64)
        if err != nil {
            panic(fmt.Errorf("invalid X coordinate: %q", fields[6]))
        }
        y, err := strconv.ParseFloat(fields[7], 64)
        if err != nil {
            panic(fmt.Errorf("invalid Y coordinate: %q", fields[7]))
        }
        z, err := strconv.ParseFloat(fields[8], 64)
        if err != nil {
            panic(fmt.Errorf("invalid Z coordinate: %q", fields[8]))
        }

        // Write the validated and parsed fields to the CSV file as a new record
        writer.Write([]string{strconv.Itoa(atomNum), fields[3], fields[4], strconv.FormatFloat(x, 'f', -1, 64), strconv.FormatFloat(y, 'f', -1, 64), strconv.FormatFloat(z, 'f', -1, 64), fields[2]})
    }

    // Flush the writer and check for errors
    writer.Flush()
    if err = writer.Error(); err != nil {
        panic(err)
    }
}

