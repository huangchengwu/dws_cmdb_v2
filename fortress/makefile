run:
	make build_mac
	make build_linux
	./package/mac/webshell 

	

build_mac:
	../../bin/go-bindata -o=./asset/asset.go -pkg=asset    template/ static/ static/js/ static/css/
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -o   package/mac/webshell  cmd/main.go  


build_linux:
	../../bin/go-bindata -o=./asset/asset.go -pkg=asset    template/ static/ static/js/ static/css/
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o   package/linux/webshell  cmd/main.go  

