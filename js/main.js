document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const body = document.body;

    // 点击汉堡菜单切换导航栏
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
        body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
    });

    // 点击导航链接关闭菜单
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
            body.style.overflow = '';
        });
    });

    // 点击页面其他区域关闭菜单
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.nav-links') && 
            !event.target.closest('.hamburger') && 
            navLinks.classList.contains('active')) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
            body.style.overflow = '';
        }
    });

    // 视频预览点击处理
    const videoPlaceholder = document.getElementById('videoPlaceholder');
    const videoFrame = document.getElementById('videoFrame');
    const previewVideo = document.getElementById('previewVideo');

    if (videoPlaceholder) {
        videoPlaceholder.addEventListener('click', function() {
            videoPlaceholder.style.display = 'none';
            videoFrame.style.display = 'block';
            // 开始播放视频
            previewVideo.play();
        });
    }

    // 点击视频外部区域暂停播放
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.video-wrapper')) {
            if (previewVideo && !previewVideo.paused) {
                previewVideo.pause();
            }
        }
    });

    // 资源页面视频播放处理
    const videoPlaceholders = document.querySelectorAll('[id^="videoPlaceholder"]');
    
    videoPlaceholders.forEach((placeholder, index) => {
        const frameId = `videoFrame${index + 1}`;
        const videoId = `previewVideo${index + 1}`;
        
        const videoFrame = document.getElementById(frameId);
        const video = document.getElementById(videoId);
        
        if (placeholder && videoFrame && video) {
            placeholder.addEventListener('click', function() {
                placeholder.style.display = 'none';
                videoFrame.style.display = 'block';
                video.play();
            });
        }
    });

    // 点击视频外部区域暂停所有视频
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.video-thumbnail')) {
            document.querySelectorAll('[id^="previewVideo"]').forEach(video => {
                if (video && !video.paused) {
                    video.pause();
                }
            });
        }
    });
}); 
