#ifndef FFMPEG_CAPTURE_H
#define FFMPEG_CAPTURE_H

#define __STDC_CONSTANT_MACROS

#include<iostream>
#include <opencv2/opencv.hpp>

extern "C"
{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswscale/swscale.h>
#include <libavdevice/avdevice.h>
};

class ffmpegCapture {
  private:
    AVFormatContext	  *pFormatCtx;
    AVCodecContext 	  *pCodecCtx;
    AVCodec		      	*pCodec;
    AVFrame           *pFrame;
    AVFrame           *pFrameRGB;
    AVInputFormat     *ifmt;
    AVPacket          packet;
    struct SwsContext *img_convert_ctx;
    int				        i, videoindex, device_id, ret;
    int               numBytes;
    int               frameFinished;
    uint8_t           *buffer;
    char              device_name[30];

    void openCamera(void);
    void openStream(void);

  public:
    ffmpegCapture(int);
    cv::Mat read_frame(void);
    ~ffmpegCapture();
};

#endif
