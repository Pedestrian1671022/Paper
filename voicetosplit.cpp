#include <alsa/asoundlib.h>
#include <iostream>
using namespace std;


const char* origin_voice = "capturedVoice.wav";

typedef struct _wave_pcm_hdr
{
    char    riff[4];
    int     size_8;
    char    wave[4];
    char    fmt[4];
    int     fmt_size;
    short int format_tag;
    short int channels;
    int     samples_per_sec;
    int     avg_bytes_per_sec; 
    short int block_align;
    short int bits_per_sample;
    char    data[4];
    int     data_size;
} wave_pcm_hdr;

wave_pcm_hdr default_wav_hdr = 
{
    { 'R', 'I', 'F', 'F' },
    0,
    {'W', 'A', 'V', 'E'},
    {'f', 'm', 't', ' '},
    16,
    1,
    1,
    16000,
    32000,
    2,
    16,
    {'d', 'a', 't', 'a'},
    0  
};

void voice_to_split()
{
    FILE *fp = fopen(origin_voice,"rb");
    fseek(fp,0,SEEK_END);
    long len = ftell(fp);
    len = len - 44;
    fseek(fp, 44, SEEK_SET);
    char* buffer = (char*)malloc(4);
    FILE *fp_left = fopen("left.wav","wb");
    fwrite(&default_wav_hdr,sizeof(default_wav_hdr ),1,fp_left);
    FILE *fp_right = fopen("right.wav","wb");
    fwrite(&default_wav_hdr,sizeof(default_wav_hdr ),1,fp_right);
    for(int i = 0; i < len/4; i += 1)
    {
    	fread(buffer, 1, 4, fp);
    	fwrite(buffer, 1, 2, fp_left);
    	fwrite(buffer+2, 1, 2, fp_right);
    	default_wav_hdr.data_size+=2;
    }
    default_wav_hdr.size_8+=default_wav_hdr.data_size+(sizeof(default_wav_hdr)-8);
    fseek(fp_left, 4, 0);
    fseek(fp_right, 4, 0);
    fwrite(&default_wav_hdr.size_8,sizeof(default_wav_hdr.size_8),1,fp_left);
    fwrite(&default_wav_hdr.size_8,sizeof(default_wav_hdr.size_8),1,fp_right);
    fseek(fp_left, 40, 0);
    fseek(fp_right, 40, 0);
    fwrite(&default_wav_hdr.data_size,sizeof(default_wav_hdr.data_size),1,fp_left);
    fwrite(&default_wav_hdr.data_size,sizeof(default_wav_hdr.data_size),1,fp_right);
}

int main( int argv, char **argc )
{
    cout<<"开始分离声音!"<<endl;
    voice_to_split();
    return 0;
}
