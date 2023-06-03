const {createApp} = Vue
createApp({
    data(){
        return{
            appID: 1907478231,
            server: 'wss://webliveroom1907478231-api.imzego.com/ws',
            userID: '',
            userName: 'Jack Zhang',
            roomID: 'wm100',
            token: '',
            activeName: 'first',
            online_user: [],
            chatInfo: [],
            onlineTask: '',
            chatTask: '',
            content: '',
            zg: null
        }
    },
    mounted() {
        this.getTokenFn();
        //定时人物监听在线用户列表
        this.onlineTask = setInterval(this.onlineUser, 5000);
        this.chatTask = setInterval(this.chatInfoFn, 3000);
        // 初始化实例
        this.zg = new ZegoExpressEngine(this.appID, this.server);
        this.zg.setDebugVerbose(false)

        // 流状态更新回调
        this.zg.on('roomStreamUpdate', async (roomID, updateType, streamList, extendedData) => {
            // 当 updateType 为 ADD 时，代表有音视频流新增，此时可以调用 startPlayingStream 接口拉取播放该音视频流
            if (updateType == 'ADD') {
                // 与房间连接成功，只有当房间状态是连接成功时，才能进行推流、拉流等操作。
                // 创建流、预览
                // 调用 createStream 接口后，需要等待 ZEGO 服务器返回流媒体对象才能执行后续操作
                const remoteStream = await this.zg.startPlayingStream("192313213");
                // 创建媒体流播放组件对象，用于播放远端媒体流 。
                const remoteView = this.zg.createRemoteStreamView(remoteStream);
                // 将播放组件挂载到页面，"remote-video" 为组件容器 <div> 元素的 id 。
                remoteView.play("player-video");

                const remoteStream2 = await this.zg.startPlayingStream("192313217");
                // 创建媒体流播放组件对象，用于播放远端媒体流 。
                const remoteView2 = this.zg.createRemoteStreamView(remoteStream2);
                // 将播放组件挂载到页面，"remote-video" 为组件容器 <div> 元素的 id 。
                remoteView2.play("player-audio");

            } else if (updateType == 'DELETE') {
                this.zg.stopPlayingStream("192313217");
                this.zg.stopPlayingStream("192313213");
            }
        });

        // 注册弹幕通知
        this.zg.on('IMRecvBarrageMessage', async (roomID, messageInfo) =>{
            console.log("弹幕通知");
            console.log(roomID);
            console.log(messageInfo);
        })

        setTimeout(this.loginRoom, 5000);
    },
    methods: {
        loginRoom(){
            this.zg.loginRoom(this.roomID, this.token, {userID:this.userID, userName: this.userName }, { userUpdate: true }).then(async result => {
                if (result == true) {

                }
            });
        },
         onlineUser() {
             let self = this;
             axios.get('/online/')
            .then(function (response) {
                if(response.status===200){
                  self.online_user = response.data
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        chatInfoFn() {
             let self = this;
             axios.get('/chatInfo/')
            .then(function (response) {
                if(response.status===200){
                  self.chatInfo = response.data
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        sendChatFn() {
             let self = this;
             if(self.content.length > 0){
                 let rq_url = '/sendChat/?content=' + this.content
                 axios.get(rq_url)
                .then(function (response) {
                    if(response.status===200){
                        self.chatInfoFn();
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
                self.content = ''
             }
        },
        getTokenFn(){
            let self = this;
            axios.get("/token/")
            .then(function (response) {
                if(response.status===200){
                    self.token = response.data.token;
                    self.userID = response.data.userId;
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        sendBroadcastMsg(){
            this.zg.sendBarrageMessage(this.roomID, "调试消息");
        }
    }
}).use(ElementPlus).mount('#anchor-layout')