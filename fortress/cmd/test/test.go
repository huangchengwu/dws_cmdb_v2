package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"time"
)

func main() {
	// 用户密码
	userPassword := "XEFCJ9DeR7tZIMJy64"

	// 密钥
	key := "iQoH1u3H+0R/BPqbSEE83MzbQHEinn8W8fWEzLpfuzP8EIF3Qa35mEd+Fe0tBCi2TUcKzIyOckFKsZ5ydJzKBQ=="

	// 当前时间戳
	timestamp := time.Now().Unix()

	// 拼接用户密码、密钥和时间戳
	data := userPassword + "dws_cmdb" + key + fmt.Sprint(timestamp) + "@@"

	// 计算MD5哈希值
	hasher := md5.New()
	hasher.Write([]byte(data))
	hash := hex.EncodeToString(hasher.Sum(nil))

	fmt.Println("MD5哈希值:", hash)

	// 时间戳和登录密钥
	timeLoginKey := fmt.Sprint(timestamp) + " " + hash
	fmt.Println(timeLoginKey)
}
