/* ------------------------------------------------------------------
 * Copyright (C) 2009 Martin Storsjo
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied.
 * See the License for the specific language governing permissions
 * and limitations under the License.
 * -------------------------------------------------------------------
 */

#include "amr-dec.h"

/* From pvamrwbdecoder_api.h, by dividing by 8 and rounding up */
extern "C" {
	AMRRet* LittleAmrwb(const char *raw_data, const int data_len) {
		const int sizes[] = {17, 23, 32, 36, 40, 46, 50, 58, 60, 5, -1, -1, -1, -1, -1, 0};
		std::vector<uint8_t> *p_result = new std::vector<uint8_t>();;
		int offset = 0;
		char header[9];
		//fprintf(stderr, "\ndata length: %d\n", data_len);
		if (data_len <= 9) {
			AMRRet* ret = new AMRRet(nullptr, 0);
			return ret;
		}
		memcpy(header, raw_data, sizeof(header));
		if (memcmp(header, "#!AMR-WB\n", 9)) {
			fprintf(stderr, "Bad header\n");
			AMRRet* ret = new AMRRet(nullptr, 0);
			return ret;
		}
		void* amr = D_IF_init();
		offset += sizeof(header);
		while(1) {
			uint8_t buffer[500], littleendian[640], *ptr;
			int size, i;
			int16_t outbuffer[320];
			/* Find the packet size */
			if (offset < data_len) {
				memcpy(buffer, raw_data + offset, sizeof(char));
				++offset;
				size = sizes[buffer[0] >> 3 & 0x0f];
			}
			else {
				break;
			}
			if (size < 0) break;
			/* Read the mode byte */
			if (offset < (data_len - size)) {
				memcpy(buffer + 1, raw_data + offset, size * sizeof(uint8_t));
				offset += size;
			}
			else {
				break;
			}

			/* Decode the packet */
			D_IF_decode(amr, buffer, outbuffer, 0);

			/* Convert to little endian and write to wav */
			ptr = littleendian;
			for (i = 0; i < 320; i++) {
				*ptr++ = (outbuffer[i] >> 0) & 0xff;
				*ptr++ = (outbuffer[i] >> 8) & 0xff;
			}
			p_result->insert(p_result->end(), littleendian, littleendian + sizeof(littleendian));
		}
		unsigned int ret_size = p_result->size() * sizeof(uint8_t);
		char *ret = new char[ret_size];
		memcpy(ret, p_result->data(), ret_size);
		AMRRet *ret_result = new AMRRet(ret, ret_size);
		D_IF_exit(amr);
		delete p_result;
		return ret_result;
	}
}

