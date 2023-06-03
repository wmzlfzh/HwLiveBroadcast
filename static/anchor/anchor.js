const {createApp} = Vue
createApp({
    data(){
        return{
            videoStream: '',
            audioStream: '',
            zg: null,
            activeName: 'first',
            online_user: [],
            chatInfo: [],
            onlineTask: '',
            chatTask: '',
            content: '',
            appID: 0,
            server: '',
            token: '',
            userID: '',
            videoID: '',
            audioID: '',
            playType: 0
        }
    },
    mounted() {
        // 获取房间ID
        this.roomID = this.geturlParm('roomID')
        // 获取其他参数
        this.getUserConfig()

        window.addEventListener('unload', this.closePage);
        // window.addEventListener('load', this.loadPage);

        //定时人物监听在线用户列表
        this.onlineTask = setInterval(this.onlineUser, 5000);
        this.chatTask = setInterval(this.getChatInfo, 3000);

        // 延迟5秒再登录
        setTimeout(this.initAndLoginRoom, 5000);

    },
    methods: {
        async loadPage(){
            console.log('加载页面')
            await axios.get('/live/refresh/?op=add&roomID=' + this.roomID + '&userID=' + this.userID);
        },
        async closePage(){
            console.log('离开页面')
            await axios.get('/live/refresh/?op=close&roomID=' + this.roomID + '&userID=' + this.userID);
        },
        // 获取Url参数
        geturlParm(name){
            let geturl = window.location.href
            let info = geturl.split('?')[1]
            let infoParams = new URLSearchParams('?'+info)
            return infoParams.get(name)
        },
        // 获取用户视频配置
         getUserConfig(){
            let self = this;
            axios.get('/live/admin/config/?roomID=' + this.roomID).then(response =>{
                if(response.data.code ===200){
                    console.log(response.data.data)
                    self.appID = response.data.data.appID
                    self.server = response.data.data.server
                    self.videoID = response.data.data.videoID
                    self.audioID = response.data.data.audioID
                    self.token = response.data.data.token
                    self.userID = response.data.data.userID
                }
            });
        },
        // 初始化并登录房间
        initAndLoginRoom(){
            // 初始化实例
            this.zg = new ZegoExpressEngine(this.appID, this.server);
            // 是否错误弹窗
            this.zg.setDebugVerbose(false);
            // 登录房间
            this.zg.loginRoom(this.roomID, this.token, {userID: this.userID, userName: this.userName}, {userUpdate: true}).then(async _result => {

            })
        },
        //开始视频直播
        async startVideoPlay(){
            // 创建流、预览
            // 调用 createStream 接口后，需要等待 ZEGO 服务器返回流媒体对象才能执行后续操作
            this.videoStream = await this.zg.createStream({camera: {video: true, audio: true}});
            // 创建媒体流播放组件
            const videoView = this.zg.createLocalStreamView(this.videoStream);
            videoView.play("play-video");
            // 开始推流，将自己的音视频流推送到 ZEGO 音视频云，此处 streamID 由用户定义，需全局唯一
            this.zg.startPublishingStream(this.videoID, this.videoStream)
            this.playType = 1
        },
        //打开投屏
        async startVideoAndAudio(){
            console.log("开始窗口直播")
            // 创建流、预览
            // 调用 createStream 接口后，需要等待 ZEGO 服务器返回流媒体对象才能执行后续操作
            this.videoStream = await this.zg.createStream({
                screen: {
                    audio: true,
                    videoQuality: 1,
                    bitRate: 1500,
                    frameRate: 15,
                },
            });
            // this.videoStream = await this.zg.createStream({source: audio})
            // 创建媒体流播放组件
            const videoView = this.zg.createLocalStreamView(this.videoStream);
            videoView.play("play-video");
            // 开始推流，将自己的音视频流推送到 ZEGO 音视频云，此处 streamID 由用户定义，需全局唯一
            this.zg.startPublishingStream(this.videoID, this.videoStream)

        },

        //关闭投屏
        stopVideo(){
            // 根据本端 streamID 停止推流
            this.zg.stopPublishingStream(this.videoID)
            // localStream 是调用 createStream 接口获取的 MediaStream 对象
            this.zg.destroyStream(this.videoStream)
        },

        // 打开麦克风
        async startAudio(){
            this.audioStream = await this.zg.createStream({camera: {video: false, audio: true}});
            // 开始推流，将自己的音视频流推送到 ZEGO 音视频云，此处 streamID 由用户定义，需全局唯一
            this.zg.startPublishingStream(this.audioID, this.audioStream)
        },
        //关闭麦克风
        stopAudio() {
             // 根据本端 streamID 停止推流
            this.zg.stopPublishingStream(this.audioID)
            // localStream 是调用 createStream 接口获取的 MediaStream 对象
            this.zg.destroyStream(this.audioStream)
        },
        //关闭直播
        stopPlay(){
            console.log("关闭窗口直播")

            // 根据本端 streamID 停止推流
            this.zg.stopPublishingStream(this.videoID)
            // localStream 是调用 createStream 接口获取的 MediaStream 对象
            this.zg.destroyStream(this.videoStream)

            if(this.playType === 2) {
                // 根据本端 streamID 停止推流
                this.zg.stopPublishingStream(this.audioID)
                // localStream 是调用 createStream 接口获取的 MediaStream 对象
                this.zg.destroyStream(this.audioStream)
            }
            axios.get('/live/admin/stop/?roomID=' + this.roomID)
        },
        // 在线用户
        async onlineUser() {
            let rst = await axios.get('/live/online/?roomID='+ this.roomID)
            this.online_user = rst.data
        },
        // 聊天信息
        async getChatInfo() {
            let rst = await axios.get('/live/chat/?roomID='+ this.roomID)
            this.chatInfo = rst.data

            this.handleClick()
        },
        // 发送聊天信息
        sendImInfo(){
            axios.get('/live/chat/send/?roomID=' + this.roomID +'&userID=' + this.userID + '&content=' +this.content);
            this.content = '';
            this.chatInfoFn();
        },

        // 聊天滚动条
        handleClick() {
            this.$nextTick(() => {
                if (this.$refs.innerRef.clientHeight > 200) {
                    this.$refs.scrollbarRef.setScrollTop(this.$refs.innerRef.clientHeight);
                }
            })
        }
    }
}).use(ElementPlus).mount('#anchor-layout')