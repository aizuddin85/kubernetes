## How to build 

For GCR, ensure JSON key is provided and access to registry is properly configured.  

1. Ensure gpgme library install  
a. apt-get install libgpgme-dev  
b. dnf install gpgme-devel  

2. Update modules `go mod tidy`  

3. To run the directly, execute `go run main.go` 
 
4. To build the binary, execute `go build -o sync_registries`

5. Run `sync_registries` to begin sync.
