#include <WinSock2.h>
#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include<tchar.h>
 
#pragma comment(lib,"ws2_32")
//
// http://www.njupt.edu.cn/abc/a.html
//
void url_spider(const char *pszUrl, const char *pszFile) {
 
	char  szHost[256];
	char  *Ptr = (char*)pszUrl;
	if (0 != ::_strnicmp(Ptr, "http://", 7)) {			//extern int strnicmp(char *str1,char * str2，int n)：比较字符串str1和str2的前n个字符串字典序的大小，但是不区分字母大小写。
 
														//返回说明：返回整数值：当str1 < str2时，返回值<0； 当str1 = str2时，返回值 = 0； 当str1>str2时，返回值>0
		printf("Oops, invalid url:[%s]\r\n", Ptr);
		return;
	}
	Ptr += 7;
	int i = 0;
	while (i < 255 && *Ptr && *Ptr != '/') {
		szHost[i++] = *Ptr++;		//szHost存的是www.njupt.edu.cn  *p = *(p+1)//优先级相同按从左到右的顺序 先*后++; 
	}
	szHost[i] = '\0';
	char  *Buffer = new char[1024 * 8];
	i = sprintf(Buffer,
		"GET %s HTTP/1.1\r\n"
		"Host: %s\r\n"
		"User-Agent: IE or Chrome\r\n"
		"Accept-Type: */*\r\n"
		"Connection: Close\r\n\r\n",
		Ptr,						//Ptr=/
		szHost					//?Q：这里为什么要传两个参数
	);
	printf("%s", Buffer);
 
	SOCKET fd = socket(AF_INET, SOCK_STREAM, 0);
	SOCKADDR_IN addr;
	addr.sin_addr.S_un.S_addr = 0;
	addr.sin_port = htons(0);
	addr.sin_family = AF_INET;
	i = bind(fd, (const sockaddr*)&addr, sizeof(SOCKADDR_IN));
	//
	// dns resolving
	//
	hostent *p = ::gethostbyname(szHost);					//gethostbyname()返回对应于给定主机名的包含主机名字和地址信息的hostent结构指针。非空指针——成功，空指针——出错，同时设置h_errno
	if (p) {
		ULONG ai = *(ULONG*)p->h_addr_list[0];//hostent->h_addr_list表示的是主机的ip地址。是网络字节序，需要通过inet_ntop函数转换。
		addr.sin_addr.S_un.S_addr = ai;
		addr.sin_port = htons(80);
		i = connect(fd, (const sockaddr*)&addr, sizeof(SOCKADDR_IN));
		if (i == NOERROR) {
			//
			// send HTTP request to our server
			//
			i = send(fd, (const char*)Buffer, (int)strlen(Buffer), 0);
			FILE *pf = fopen(pszFile, "wb");
			do {
				i = recv(fd, Buffer, 8191, 0);
				if (i <= 0) {
					break;
				}
				Buffer[i] = '\0';
				fwrite(Buffer, 1, i, pf);
				printf("%s", Buffer);
			} while (TRUE);
			fclose(pf);
		}
		else {
			printf("Failed to connect [%s]\r\n", szHost);
		}
	}
	else {
		printf("Failed to resolve [%s]\r\n", szHost);
	}
	closesocket(fd);
	delete[]Buffer;
 
	return;
}
int _tmain(int argc, _TCHAR* argv[])
{
	WSADATA  wsaData;
	//
	// Loading ws2_32.dll module into process address map
	//
	WSAStartup(0x0202, &wsaData);
 
	//
	// TODO ? 
	//
	url_spider("http://www.njupt.edu.cn/", "abc.txt");
	url_spider("http://www.njupt.edu.cn/8/list.htm", "abc.txt");
	WinExec("notepad.exe abc.txt", SW_NORMAL);
 
 
	getchar();
	//
	// Unload(aka dump out) this module from process address map
	//
	WSACleanup();
	return 0;
}

