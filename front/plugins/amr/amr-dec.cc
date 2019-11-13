#include "amr-dec.h"

extern "C" {
	void FreeAMRRet(const AMRRet *buffer) {
		delete buffer;
		buffer = NULL;
	}

}
