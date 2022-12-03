package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "strings"
)

func main() {
    // Open the input file
    inputFile, err := os.Open(os.Args[1])
    if err != nil {
        log.Fatal(err)
    }
    defer inputFile.Close()

    // Create a new scanner to read the input file
    scanner := bufio.NewScanner(inputFile)

    // Read the first line containing the title
    scanner.Scan()
    title := strings.TrimSpace(scanner.Text())

    // Read the second line containing the element symbols and their counts
    scanner.Scan()
    line := strings.TrimSpace(scanner.Text())
    symbols, counts := line[:strings.Index(line, "from")], line[strings.Index(line, "from"):]

    // Read the remaining lines containing the coordinates
    var coordinates [][]string
    for scanner.Scan() {
        line = strings.TrimSpace(scanner.Text())
        if line != "" {  // skip empty lines
            elements := strings.Fields(line)
            coordinates = append(coordinates, elements)
        }
    }

    // Open the output file
    outputFile, err := os.Create("output.POSCAR")
    if err != nil {
        log.Fatal(err)
    }
    defer outputFile.Close()

    // Create a new writer to write to the output file
    writer := bufio.NewWriter(outputFile)

    // Write the title
    fmt.Fprintln(writer, title)

    // Write the scaling factor
    fmt.Fprintln(writer, "1.0")

    // Write the lattice vectors
    fmt.Fprintln(writer, "10 0 0")
    fmt.Fprintln(writer, "0 10 0")
    fmt.Fprintln(writer, "0 0 10")

    // Write the element symbols and their counts
    fmt.Fprintln(writer, symbols)
    fmt.Fprintln(writer, counts)

    // Write the coordinate system
    fmt.Fprintln(writer, "Cartesian")

    // Write the coordinates
    for _, elements := range coordinates {
        fmt.Fprintf(writer, "%s %s %s %s\n", elements[1], elements[2], elements[3], elements[0])
    }

    // Flush the writer to ensure that all data is written to the output file
    writer.Flush()

    // Check if there was an error while scanning the input file
    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }

    // Check if there was an error while writing to the output file
    if err := writer.Flush(); err != nil {
        log.Fatal(err)
    }



}