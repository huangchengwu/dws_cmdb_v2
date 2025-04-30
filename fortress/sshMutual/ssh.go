package sshMutual

import (
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"

	"github.com/creack/pty"
	"golang.org/x/crypto/ssh"
	"golang.org/x/crypto/ssh/terminal"
)

func publicKeyAuthFunc(kPath []byte) ssh.AuthMethod {
	log.Println("===", string(kPath))
	signer, err := ssh.ParsePrivateKey(kPath)
	if err != nil {
		log.Fatal("ssh 关键签名失败", err)
	}
	return ssh.PublicKeys(signer)
}
func (c *ssh_client) Ssh_key_Ping() bool {

	sshPort := 2260

	config := &ssh.ClientConfig{
		Timeout:         time.Second,
		User:            c.userinfo.Username,
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	config.Auth = []ssh.AuthMethod{publicKeyAuthFunc([]byte(c.userinfo.Host_key))}

	addr := fmt.Sprintf("%s:%d", c.userinfo.Host, sshPort)
	if c.cli, c.err = ssh.Dial("tcp", addr, config); c.err != nil {

		log.Println("===链接失败错误", c.err)
		c.cli.Close()
		return false
	}
	log.Println(c.userinfo.Host, c.userinfo.Username, c.userinfo.Password, "连接成功", c.err)
	return true
}

// 检测连接请求是否可用
func (c *ssh_client) Ping() bool {
	cs := &ssh.ClientConfig{
		User:    c.userinfo.Username,
		Timeout: 5 * time.Second,
		Auth: []ssh.AuthMethod{
			ssh.Password(c.userinfo.Password),
		},
		HostKeyCallback: func(hostname string, remote net.Addr, key ssh.PublicKey) error {
			return nil
		},
	}

	if c.cli, c.err = ssh.Dial("tcp", c.userinfo.Host, cs); c.err != nil {
		log.Println("===链接失败错误", c.err, c.userinfo)
		c.cli.Close()
		return false
	}

	log.Println(c.userinfo.Host, c.userinfo.Username, c.userinfo.Password, "连接成功", c.err)
	return true

}

func (c *ssh_client) NewLocalHost(cmd string, arg ...string) {
	log.Println(cmd, arg)
	cs := exec.Command(cmd, arg...)

	c.ptmx, _ = pty.Start(cs)
	defer c.ptmx.Close()
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGWINCH)
	go func() {
		for range ch {
			if err := pty.InheritSize(os.Stdin, c.ptmx); err != nil {
				log.Printf("error resizing pty: %s", err)
			}
		}
	}()
	ch <- syscall.SIGWINCH
	oldState, _ := terminal.MakeRaw(int(os.Stdin.Fd()))

	terminal.Restore(int(os.Stdin.Fd()), oldState)
	cs.Wait()

	log.Println("~~~~~~~~~~终端退出")

}

// 开启会话
func (c *ssh_client) NewSession(cmd string) {
	if c.session, c.err = c.cli.NewSession(); c.err != nil {
		log.Println("会话开启失败", c.err)

	}
	defer c.session.Close()
	fd := int(os.Stdin.Fd())
	c.oldState, c.err = terminal.MakeRaw(fd)
	defer terminal.Restore(fd, c.oldState)

	c.Stdout, c.err = c.session.StdoutPipe()

	c.Stdin, c.err = c.session.StdinPipe()
	// c.Stderr, c.err = c.session.StderrPipe()

	modes := ssh.TerminalModes{
		ssh.ECHO:          1,
		ssh.TTY_OP_ISPEED: 14400,
		ssh.TTY_OP_OSPEED: 14400,
	}

	c.session.RequestPty("xterm-256color", c.userinfo.Height, c.userinfo.Width, modes)
	c.session.Run(cmd)

}
