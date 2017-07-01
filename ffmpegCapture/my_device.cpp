#include <stdio.h>
#include<iostream>
#define __STDC_CONSTANT_MACROS

extern "C"
{

#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswscale/swscale.h>
#include <libavdevice/avdevice.h>

};

#include <opencv2/opencv.hpp>

int main(int argc, char* argv[])
{
  AVFormatContext	*pFormatCtx;
	int				      i, videoindex;
	AVCodecContext 	*pCodecCtx;
	AVCodec		     	*pCodec;
  AVFrame           *pFrame = NULL;
  AVFrame           *pFrameRGB = NULL;
  AVPacket          packet;
  int               numBytes;
  uint8_t           *buffer = NULL;
  int               frameFinished;

  av_register_all();
	avformat_network_init();
	pFormatCtx = avformat_alloc_context();
  //Register Device
	avdevice_register_all();

  //Linux
  AVInputFormat *ifmt=av_find_input_format("video4linux2");
  if(avformat_open_input(&pFormatCtx,"/dev/video1",ifmt,NULL)!=0){
    printf("Couldn't open input stream.\n");
    return -1;
  }

  if(avformat_find_stream_info(pFormatCtx,NULL)<0)
  {
    printf("Couldn't find stream information.\n");
    return -1;
  }

  videoindex=-1;
	for(i=0; i<pFormatCtx->nb_streams; i++)
		if(pFormatCtx->streams[i]->codec->codec_type==AVMEDIA_TYPE_VIDEO)
		{
			videoindex=i;
			break;
		}
	if(videoindex==-1)
	{
		printf("Couldn't find a video stream.\n");
		return -1;
	}

  pCodecCtx=pFormatCtx->streams[videoindex]->codec;
	pCodec=avcodec_find_decoder(pCodecCtx->codec_id);
	if(pCodec==NULL)
	{
		printf("Codec not found.\n");
		return -1;
	}
  //pCodecCtx = avcodec_alloc_context3(pCodec);
	if(avcodec_open2(pCodecCtx, pCodec,NULL)<0)
	{
		printf("Could not open codec.\n");
		return -1;
	}

  // Allocate video frame
  pFrame=av_frame_alloc();

  // Allocate an AVFrame structure
  pFrameRGB=av_frame_alloc();
  if(pFrameRGB==NULL)
  {
		printf("RGB not allocated.\n");
		return -1;
	}
  // Determine required buffer size and allocate buffer
  numBytes=avpicture_get_size(AV_PIX_FMT_BGR24, pCodecCtx->width,
			      pCodecCtx->height);
  buffer=(uint8_t *)av_malloc(numBytes*sizeof(uint8_t));

  // Assign appropriate parts of buffer to image planes in pFrameRGB
  // Note that pFrameRGB is an AVFrame, but AVFrame is a superset
  // of AVPicture
  avpicture_fill((AVPicture *)pFrameRGB, buffer, AV_PIX_FMT_BGR24,
		 pCodecCtx->width, pCodecCtx->height);

  struct SwsContext *img_convert_ctx;
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
  // Read frames and save first five frames to disk
  while(true) {
    if(av_read_frame(pFormatCtx, &packet)>=0){
      // Is this a packet from the video stream?
      if(packet.stream_index==videoindex) {
        // Decode video frame
        avcodec_decode_video2(pCodecCtx, pFrame, &frameFinished, &packet);

        // Did we get a video frame?
        if(frameFinished){
          sws_scale(img_convert_ctx, (uint8_t const * const *)pFrame->data,
              pFrame->linesize, 0, pCodecCtx->height,pFrameRGB->data, pFrameRGB->linesize);
          cv::Mat img(pCodecCtx->height,pCodecCtx->width,CV_8UC3,pFrameRGB->data[0]);
          cv::imshow("orig",img);
        }
      }
      // Free the packet that was allocated by av_read_frame
      av_free_packet(&packet);
    }
    if(cv::waitKey(30) >= 27) break;
  }

  av_free(buffer);
  av_free(pFrame);
  av_free(pFrameRGB);
  avcodec_close(pCodecCtx);
  avformat_close_input(&pFormatCtx);

  return 0;
}
