#include "kaldi-nnet3-online-decoder.h"

static netease::KaldiNnet3ParallelableDecoder decoder;
extern "C" {
bool InitDecoder(const char* c_config_filename,
                 const char* c_fst_rxfilename,
                 const char* c_word2int_rxfilename,
                 const char* c_am_model_rxfilename) {
  const std::string config_filename(c_config_filename), fst_rxfilename(c_fst_rxfilename),
                    word2int_rxfilename(c_word2int_rxfilename),am_model_rxfilename(c_am_model_rxfilename);
  if (!decoder.IsInit()){
    return decoder.Init(config_filename, fst_rxfilename, word2int_rxfilename, am_model_rxfilename);
  } else {
    KALDI_WARN << "Decoder had been init yet.";
    return false;
  }
}

bool DecodeWavAsync(const char *c_utt, 
                    const char *raw_data,
                    const uint32 wav_len,
                    bool (*callback_func)(const char*, const char *)) {
  if (decoder.IsInit()){
    const std::string utt(c_utt);
    // 注意大端和小端
    const short *wav_data = (const short*)raw_data;
    std::string decode_result = decoder.DecodeText(utt, wav_data, wav_len);
    return callback_func(c_utt, decode_result.c_str());
  }
  else {
    KALDI_WARN << "Decoder not init yet.";
    return false;
  }
}

const char* DecodeWavSync(const char *c_utt, 
                          const char *raw_data,
                          const uint32 wav_len) {
  const std::string utt(c_utt);
  std::string decode_result = "";
  if (decoder.IsInit()){
    // 注意大端和小端
    const short *wav_data = (const short*)raw_data;
    decode_result = decoder.DecodeText(utt, wav_data, wav_len);
  }
  else {
    KALDI_WARN << "Decoder not init yet.";
  }
  size_t len = strlen(decode_result.c_str());
  char *c_result = new char[len + 1];
  memset(c_result, 0, len + 1);
  strcpy(c_result, decode_result.c_str());
  return c_result;
}

void FreeDecodeBuffer(const char *buffer){
  if (buffer != NULL){
    delete buffer;
    buffer = NULL;
  }
}

}