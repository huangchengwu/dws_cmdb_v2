package main

import (
	"Fortress/asset"
	"Fortress/sshMutual"
	"html/template"
	"log"

	assetfs "github.com/elazarl/go-bindata-assetfs"
	"github.com/gin-gonic/gin"
)

func main() {

	fsCss := assetfs.AssetFS{Asset: asset.Asset, AssetDir: asset.AssetDir, AssetInfo: asset.AssetInfo, Prefix: "static/css", Fallback: "index.html"}
	fsJs := assetfs.AssetFS{Asset: asset.Asset, AssetDir: asset.AssetDir, AssetInfo: asset.AssetInfo, Prefix: "static/js", Fallback: "index.html"}
	fs := assetfs.AssetFS{Asset: asset.Asset, AssetDir: asset.AssetDir, AssetInfo: asset.AssetInfo, Prefix: "template", Fallback: "index.html"}

	go sshMutual.NewConnectServer()

	r := gin.Default()

	r.StaticFS("static/css", &fsCss)
	r.StaticFS("static/js", &fsJs)
	r.StaticFS("template", &fs)

	r.GET("/", func(c *gin.Context) {
		indexHtml, err := asset.Asset("template/index.html")
		if err != nil {
			log.Println(err)
		}
		tmpl, err := template.New("index").Parse(string(indexHtml))

		if err != nil {
			log.Println(err)
		}
		c.Status(200)
		tmpl.Execute(c.Writer, struct{ Title string }{Title: "webshell"})

	})

	r.Run(":8081")
}
