#include <stdio.h>
#include<iostream>
#include <opencv2/opencv.hpp>

#define __STDC_CONSTANT_MACROS

extern "C"
{

#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswscale/swscale.h>
#include <libavdevice/avdevice.h>

};

using namespace std;

class ffmpegCapture {
  private:
    AVFormatContext	  *pFormatCtx;
    AVCodecContext 	  *pCodecCtx;
    AVCodec		      	*pCodec;
    AVFrame           *pFrame = NULL;
    AVFrame           *pFrameRGB = NULL;
    AVInputFormat     *ifmt;
    AVPacket          packet;
    struct SwsContext *img_convert_ctx;
    int				        i, videoindex, device_id, ret;
    int               numBytes;
    int               frameFinished;
    uint8_t           *buffer = NULL;
    char              device_name[30];

    void openCamera(void)
    {
      ifmt = av_find_input_format("video4linux2");
      if(avformat_open_input(&pFormatCtx,device_name,ifmt,NULL)!=0){
        cout<<"Couldn't open input stream.\n"<<endl;
        ret = 1;
      }

      if(avformat_find_stream_info(pFormatCtx,NULL)<0)
      {
        cout<<"Couldn't find stream information.\n"<<endl;
        ret = 2;
      }

    }

    void openStream(void)
    {
      for(i=0; i<pFormatCtx->nb_streams; i++)
        if(pFormatCtx->streams[i]->codec->codec_type==AVMEDIA_TYPE_VIDEO)
        {
          videoindex = i;
          break;
        }
      if(videoindex == -1)
      {
        cout<<"Couldn't find a video stream.\n"<<endl;
        ret = 3;
      }

      pCodecCtx = pFormatCtx->streams[videoindex]->codec;
    	pCodec    = avcodec_find_decoder(pCodecCtx->codec_id);
    	if(pCodec == NULL)
    	{
    		cout<<"Codec not found.\n"<<endl;
    		ret = 4;
    	}
      //pCodecCtx = avcodec_alloc_context3(pCodec);
    	if(avcodec_open2(pCodecCtx, pCodec,NULL)<0)
    	{
    		cout<<"Could not open codec.\n"<<endl;
    		ret = 5;
    	}

    };

  public:
    ffmpegCapture(int id = 0)
    {

      av_register_all();
    	avformat_network_init();
    	avdevice_register_all();
    	pFormatCtx = avformat_alloc_context();
      pFrame     = av_frame_alloc();
      pFrameRGB  = av_frame_alloc();

      device_id = id;
      videoindex= -1;
      frameFinished = 0;
      ret = 0;
      sprintf(device_name, "/dev/video%d", device_id);

      openCamera();
      openStream();

      // Determine required buffer size and allocate buffer
      numBytes = avpicture_get_size(AV_PIX_FMT_BGR24, pCodecCtx->width,
    			         pCodecCtx->height);
      buffer   = (uint8_t *)av_malloc(numBytes*sizeof(uint8_t));

      avpicture_fill((AVPicture *)pFrameRGB, buffer, AV_PIX_FMT_BGR24,
    		 pCodecCtx->width, pCodecCtx->height);

     // initialize SWS context for software scaling
     img_convert_ctx = sws_getContext(pCodecCtx->width,
   			   pCodecCtx->height,
   			   pCodecCtx->pix_fmt,
   			   pCodecCtx->width,
   			   pCodecCtx->height,
   			   AV_PIX_FMT_BGR24,
   			   SWS_BILINEAR,
   			   NULL,
   			   NULL,
   			   NULL
   			   );
    }

    cv::Mat read_frame(void)
    {
      while(frameFinished == 0){
        if(av_read_frame(pFormatCtx, &packet)>=0){
          // Is this a packet from the video stream?
          if(packet.stream_index==videoindex) {
            // Decode video frame
            avcodec_decode_video2(pCodecCtx, pFrame, &frameFinished, &packet);
          }
        }
     }
     frameFinished = 0;
     sws_scale(img_convert_ctx, (uint8_t const * const *)pFrame->data,
         pFrame->linesize, 0, pCodecCtx->height,pFrameRGB->data, pFrameRGB->linesize);
     cv::Mat img(pCodecCtx->height,pCodecCtx->width,CV_8UC3,pFrameRGB->data[0]);
     // Free the packet that was allocated by av_read_frame
     av_free_packet(&packet);

     return img;
    }

    ~ffmpegCapture()
    {
      av_free(buffer);
      av_free(pFrame);
      av_free(pFrameRGB);
      avcodec_close(pCodecCtx);
      avformat_close_input(&pFormatCtx);
    }
};


int main(int argc, char *argv[])
{
  cv::Mat frame;
  ffmpegCapture cap(0);

  while(true)
  {
    frame = cap.read_frame();
    cv::imshow("display",frame);

    if(cv::waitKey(30)>=27) break;
  }

  return 0;
}
