package main

import (
    "bufio"
    "fmt"
    "os"
    "regexp"
    "strconv"
    "strings"
)

// Regular expression pattern for a valid XYZ record
var xyzRecordPattern = regexp.MustCompile(`^\s*\w+\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\s*$`)

// xyzToPoscar converts an XYZ file to a POSCAR file in cartesian format
func xyzToPoscar(xyzPath, poscarPath string) {
    // Open the XYZ file in read-only mode
    xyzFile, err := os.Open(xyzPath)
    if err != nil {
        panic(err)
    }
    defer xyzFile.Close()

    // Open the POSCAR file in write mode
    poscarFile, err := os.Create(poscarPath)
    if err != nil {
        panic(err)
    }
    defer poscarFile.Close()

    // Read the first line of the XYZ file, which contains the number of atoms
    scanner := bufio.NewScanner(xyzFile)
    scanner.Scan()
    numAtoms, err := strconv.Atoi(scanner.Text())
    if err != nil {
        panic(err)
    }

    // Read the second line of the XYZ file, which contains the comment
    scanner.Scan()
    comment := scanner.Text()

    // Write the comment to the POSCAR file
    poscarFile.WriteString(fmt.Sprintf("%s\n", comment))

    // Include the scaling factor, for now, it will just be 1
    poscarFile.WriteString(fmt.Sprintf("1\n"))

    // Make a 15x15x15 Box
    poscarFile.WriteString(fmt.Sprint("15 0  0\n0 15  0\n0  0 15\n"))


    // Read the remaining lines of the XYZ file, which contain the atom positions
    atomPositions := make([][3]float64, numAtoms)
    for i := 0; i < numAtoms; i++ {
        if !scanner.Scan() {
            panic(fmt.Errorf("Invalid number of atoms in XYZ file (expected %d)", numAtoms))
        }
        line := scanner.Text()

        // Check if the line is a valid XYZ record
        if !xyzRecordPattern.MatchString(line) {
            panic(fmt.Errorf("Invalid XYZ record on line %d: %s", i+3, line))
        }

	// Split the line into fields, and extract the atom type
 	fields := strings.Fields(line)
   	atomType := fields[0]

        // Add the atom type to the slice of atom types
   	atomTypes = append(atomTypes, atomType)

        // Split the line into fields, and convert the coordinates to floats
        x, err := strconv.ParseFloat(fields[1], 64)
        if err != nil {
            panic(err)
        }
        y, err := strconv.ParseFloat(fields[2], 64)
        if err != nil {
            panic(err)
        }
        z, err := strconv.ParseFloat(fields[3], 64)
        if err != nil {
            panic(err)
        }
        atomPositions[i] = [3]float64{x, y, z}
    }


	
    // Write the atom types to the POSCAR file
    for atomType := range atomCounts {
        poscarFile.WriteString(fmt.Sprintf("%s ", atomType))
    }
    poscarFile.WriteString("\n")

    // Write the atom counts to the POSCAR file
    for _, count := range atomCounts {
        poscarFile.WriteString(fmt.Sprintf("%d ", count))
    }
    poscarFile.WriteString("\nCartesian\n")
    for i, atomType := range atomTypes {
        // Get the atomic coordinates for the current atom type
        x, y, z := atomPositions[i][0], atomPositions[i][1], atomPositions[i][2]
    
        // Write the atom type and coordinates to the POSCAR file
        poscarFile.WriteString(fmt.Sprintf("%.6f %.6f %.6f %s\n", x, y, z, atomType))
    }

    // Print a message indicating that the POSCAR file was generated
    fmt.Printf("Generated POSCAR file from %s\n", xyzPath)
    }

func main() {
    // Convert the XYZ file specified as the first command-line argument to a POSCAR file
    // in cartesian format, with the name specified as the second command-line argument
    if len(os.Args) < 3 {
        fmt.Println("Usage: xyz_to_poscar <xyz_file> <poscar_file>")
        return
    }
    xyzFile := os.Args[1]
    poscarFile := os.Args[2]
    xyzToPoscar(xyzFile, poscarFile)
}
