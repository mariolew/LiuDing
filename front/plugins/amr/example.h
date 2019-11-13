
bool InitDecoder(const char* c_config_filename,
                 const char* c_fst_rxfilename,
                 const char* c_word2int_rxfilename,
                 const char* c_am_model_rxfilename);
bool DecodeWavAsync(const char *c_utt, 
                    const char *raw_data,
                    const uint32 wav_len,
                    bool (*callback_func)(const char*, const char *));
const char* DecodeWavSync(const char *c_utt, 
                          const char *raw_data,
                          const uint32 wav_len);
void FreeDecodeBuffer(const char *buffer);
                 