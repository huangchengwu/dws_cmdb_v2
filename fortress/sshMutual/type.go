package sshMutual

import (
	"io"
	"os"

	"github.com/gorilla/websocket"
	"golang.org/x/crypto/ssh/terminal"

	"golang.org/x/crypto/ssh"
)

type userinfo struct {
	Username  string
	Password  string
	Host      string
	Timestamp string
	Key       string
	Host_key  string
	LocalMode string
	Cmd       []string
	Height    int
	Width     int
}
type ssh_client struct {
	userinfo userinfo

	cli      *ssh.Client
	session  *ssh.Session
	oldState *terminal.State
	Stdout   io.Reader
	Stderr   io.Reader
	Stdin    io.WriteCloser
	ptmx     *os.File
	err      error
	Msg      map[string]string
}

type socketConn struct {
	Conn *websocket.Conn
	err  error
	p    []byte
}

// 客户端 Client
type Client struct {
	//用户id
	id string
	//连接的socket
	socket *websocket.Conn
	//发送的消息
	send       chan []byte
	ssh_client *ssh_client
}

// 客户端管理
type ClientManager struct {
	//客户端 map 储存并管理所有的长连接client，在线的为true，不在的为false
	clients map[*Client]bool
	//web端发送来的的message我们用broadcast来接收，并最后分发给所有的client
	//新创建的长连接client
	register chan *Client
	//新注销的长连接client
	unregister chan *Client
}
