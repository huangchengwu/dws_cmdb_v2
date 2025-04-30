package sshMutual

import (
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"time"
	"unicode/utf8"

	"github.com/gorilla/websocket"
	uuid "github.com/satori/go.uuid"
)

// 创建客户端管理者
var manager = ClientManager{
	register:   make(chan *Client),
	unregister: make(chan *Client),
	clients:    make(map[*Client]bool),
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func (manager *ClientManager) start() {
	for {

		select {
		//如果有新的连接接入,就通过channel把连接传递给conn
		case conn := <-manager.register:
			//把客户端的连接设置为true
			manager.clients[conn] = true
			//把返回连接成功的消息json格式化
			log.Println(conn.id, "连接成功")

			conn.send <- []byte(fmt.Sprintf("连接成功 当前在线用户 %d", len(manager.clients)))

			//调用客户端的send方法，发送消息
			go manager.send(conn)
			//如果连接断开了

		case conn := <-manager.unregister:
			//判断连接的状态，如果是true,就关闭send，删除连接client的值
			log.Println("conn", conn, manager.clients)
			if _, ok := manager.clients[conn]; ok {

				log.Println("关闭连接", conn.id, ok, manager.clients)
				if conn.ssh_client.cli != nil {
					log.Println("close ssh")
					conn.ssh_client.cli.Close()
				}
				if conn.ssh_client.userinfo.LocalMode == "yes" {

					log.Println("close cmd")
					conn.ssh_client.ptmx.Close()

				}

				conn.send <- []byte(fmt.Sprintf("断开成功 当前在线用户 %d", len(manager.clients)))

				conn.socket.Close()
				close(conn.send)
				delete(manager.clients, conn)
				log.Println("注销后", manager.clients)

			}
		}
	}
}

// 定义客户端管理的send方法
func (manager *ClientManager) send(c *Client) {
	for {

		buf := make([]byte, 4096)
		if c.ssh_client.userinfo.LocalMode == "yes" {

			if n1, err := c.ssh_client.ptmx.Read(buf); err != nil {
				log.Println("err====1", err)
				manager.unregister <- c
				break

			} else {

				if utf8.Valid(buf[:n1]) {
					c.send <- buf[:n1]
				} else {
					// 无效的UTF-8数据，忽略或丢弃
					log.Println("Invalid UTF-8 data received, ignoring it")
				}

			}

		} else {

			if n1, err := c.ssh_client.Stdout.Read(buf); err != nil {
				log.Println("err====2", err)

				manager.unregister <- c
				break

			} else {

				if utf8.Valid(buf[:n1]) {
					c.send <- buf[:n1]
				} else {
					// 无效的UTF-8数据，忽略或丢弃
					log.Println("Invalid UTF-8 data received, ignoring it")
				}

			}

		}

	}
}

// 定义客户端结构体的read方法
func (c *Client) read() {
	defer func() {
		manager.unregister <- c
		c.socket.Close()
	}()
	for {
		//读取消息
		_, message, err := c.socket.ReadMessage()
		//如果有错误信息，就注销这个连接然后关闭
		if err != nil {
			log.Println("err====3", err)

			manager.unregister <- c
			c.socket.Close()
			break
		}
		if c.ssh_client.userinfo.LocalMode == "yes" {
			go io.Copy(c.ssh_client.ptmx, strings.NewReader(string(message)))

		} else {

			go io.Copy(c.ssh_client.Stdin, strings.NewReader(string(message)))

		}

	}

}

func (c *Client) write() {
	defer func() {
		c.socket.Close()
	}()

	for {
		select {
		//从send里读消息
		case message, ok := <-c.send:
			//如果没有消息
			if !ok {
				c.socket.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			c.socket.WriteMessage(websocket.TextMessage, message)
		}
	}
}
func CheckLoginKey(timestamp string, login_key string) bool {
	// 用户密码
	log.Println("timestamp", timestamp, "login_key", login_key)

	userPassword := "XEFCJ9DeR7tZIMJy64"

	// 密钥
	key := "iQoH1u3H+0R/BPqbSEE83MzbQHEinn8W8fWEzLpfuzP8EIF3Qa35mEd+Fe0tBCi2TUcKzIyOckFKsZ5ydJzKBQ=="

	// 拼接用户密码、密钥和时间戳
	data := userPassword + "dws_cmdb" + key + fmt.Sprint(timestamp) + "@@"
	// 计算MD5哈希值
	hasher := md5.New()
	hasher.Write([]byte(data))
	timeLoginKey := hex.EncodeToString(hasher.Sum(nil))

	log.Println("==timeLoginKey", timeLoginKey, "==login_key", login_key)

	return timeLoginKey == login_key

}
func ConnectServer(w http.ResponseWriter, req *http.Request) {
	s := &socketConn{}
	s.Conn, s.err = upgrader.Upgrade(w, req, nil)

	uuids := uuid.NewV4().String()

	webclient := &Client{id: uuids, socket: s.Conn, send: make(chan []byte)}

	_, s.p, s.err = webclient.socket.ReadMessage()
	log.Println("====", string(s.p))
	u := userinfo{}

	if s.err = json.Unmarshal(s.p, &u); s.err != nil {
		log.Println("====error", string(s.p))

		log.Println(s.err)

	} else {
		log.Println("====yes", string(s.p))

		webclient.ssh_client = &ssh_client{userinfo: u}
		log.Println("传入信息", u, webclient.ssh_client.userinfo.LocalMode)

		if CheckLoginKey(u.Timestamp, u.Key) {

			if webclient.ssh_client.userinfo.LocalMode == "local" {
				log.Println("本地模式", u.LocalMode)
				go webclient.ssh_client.NewLocalHost(u.Cmd[0], u.Cmd[1:]...)

				manager.register <- webclient
				time.Sleep(2 * time.Second)
				//启动协程收web端传过来的消息
				go webclient.read()
				//启动协程把消息返回给web端
				go webclient.write()
			}

			if webclient.ssh_client.userinfo.LocalMode == "ssh_password" {
				log.Println("远程模式密码", u.LocalMode)

				if webclient.ssh_client.Ping() {

					go webclient.ssh_client.NewSession(u.Cmd[0])
					manager.register <- webclient
					time.Sleep(2 * time.Second)
					go webclient.read()
					//启动协程把消息返回给web端
					go webclient.write()

				} else {
					manager.clients[webclient] = true
					manager.unregister <- webclient
					webclient.socket.WriteMessage(websocket.TextMessage, []byte("连接失败"))
					webclient.socket.Close()
					return

				}

			}

			if webclient.ssh_client.userinfo.LocalMode == "host_key" {
				log.Println("使用密钥登陆", u.LocalMode)

				if webclient.ssh_client.Ssh_key_Ping() {

					go webclient.ssh_client.NewSession(u.Cmd[0])
					manager.register <- webclient
					time.Sleep(2 * time.Second)
					go webclient.read()
					//启动协程把消息返回给web端
					go webclient.write()

				} else {
					manager.clients[webclient] = true
					manager.unregister <- webclient
					webclient.socket.WriteMessage(websocket.TextMessage, []byte("连接失败"))
					webclient.socket.Close()
					return

				}

			}

		} else {
			log.Println("链接失败", manager.clients, manager.unregister)
			manager.clients[webclient] = true
			manager.unregister <- webclient
			webclient.socket.WriteMessage(websocket.TextMessage, []byte("CheckLoginKey连接失败"))
			webclient.socket.Close()
			return
		}

	}

}
func NewConnectServer() {
	go manager.start()

	log.Println("启动服务websocket会话连接服务", "0.0.0.0:3002")
	http.HandleFunc("/", ConnectServer)
	http.ListenAndServe("0.0.0.0:3002", nil)

}
