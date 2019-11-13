#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <dec_if.h>
#include <interf_dec.h>
#include <vector>

extern "C" {
	typedef struct AMRRet {
		const char *ret;
		unsigned int size;
		AMRRet(const char *_ret, unsigned int _size): ret(_ret), size(_size) {};
		~AMRRet() {
			if (ret != NULL) {
				delete [] ret;
				ret = NULL;
			}
		}
	} AMRRet;

	AMRRet* LittleAmrwb(const char *raw_data, const int data_len);
	AMRRet* LittleAmrnb(const char *raw_data, const int data_len);
	void FreeAMRRet(const AMRRet *buffer);
}
