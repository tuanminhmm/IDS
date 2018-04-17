#include <stdio.h>
#include <string.h>

#define MaxCon 800000
#define MaxLine 800
#define MaxToken 20

char inigo[MaxCon][MaxLine];
char attributes[MaxCon][MaxLine];
int countatt;
int inigoKop;


int main(int argc, char **argv)
{
	FILE *finigo, *ftrafAld, *attri;
	int i,j,point,iport,itcp,iicmp,iudp,length;
	char galdera[MaxLine];
	char galdera1[MaxLine];
	int noraino;
	int nondik2, nondik100;
	char line[MaxLine];
	char linen[800];
	char templine[800];
	char ph=',';	
	char protocol[10];
	char port[10];
	char services[100];
	int ph1,ph2;
	int fph,lph; //key to split
	char filetoHong[800];
	//Uneko konexioaren datuak
	char line1[MaxLine];
	int konZenb1;
	char hasUnea1s[MaxToken];
	int hasUnea1, hasUnea12;
	int orig_p1,resp_p1;
	char orig_h1[MaxToken], resp_h1[MaxToken];
	char duration1[MaxToken], protokoloa1[MaxToken], service1[MaxToken], flag1[MaxToken];
	
	//Aurreko konexioen datuentzat
	char line2[MaxLine];
	char line3[MaxLine];
	int konZenb2;
	char hasUnea2s[MaxToken];
	int hasUnea2, hasUnea22;
	int orig_p2,resp_p2;
	char orig_h2[MaxToken], resp_h2[MaxToken];
	char duration2[MaxToken], protokoloa2[MaxToken], service2[MaxToken], flag2[MaxToken];
	int sartuDa2;
	int check;
	
	//trafiko aldagaientzat
	int count,srv_count,serror,rerror,same_srv,diff_srv,srv_serror,srv_error,srv_diff_host;
	int same_src_port;
	float serror_rate,srv_serror_rate,rerror_rate,srv_error_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate;
	float srv_rerror_rate,same_src_port_rate;

	if (argc != 2){
	  printf("Deia: %s inigo.list\n", argv[0]);
		return(1);
	}

  //inigo.list irakurri eta gorde
  sprintf(galdera, "%s", argv[1]);
  finigo = fopen(galdera, "r");
  inigoKop = 0;
  while(!feof(finigo)){
  	fgets(line2, MaxLine, finigo);
   	line2[strlen(line2)-1] = '\0';
    strcpy(inigo[inigoKop],line2);
    inigoKop = inigoKop + 1;
  }
  fclose(finigo);
  inigoKop = inigoKop - 1; //feof-z lerro bat gehiago irakurtzen baita
  //Create Attribute
	sprintf(galdera, "attributes.txt");
	attri = fopen(galdera, "r");
	countatt = 0;
 	while(!feof(attri)){
  		fgets(line3, MaxLine, attri);
   		line2[strlen(line3)-1] = '\0';
    		strcpy(attributes[countatt],line3);
    		countatt=countatt+1;
  	}
  	fclose(attri);

	//trafiko aldagaiak kalkulatu
	nondik2=0;
	for(noraino=0; noraino<inigoKop; noraino++){
		strcpy(line1, inigo[noraino]);
		sscanf(line1, "%d %s %d %d %s %s %s %s %s %s %s",
                   &konZenb1,&hasUnea1s,&orig_p1,&resp_p1,&orig_h1,&resp_h1,
                   &duration1,&protokoloa1,&service1,&flag1);
		sscanf(hasUnea1s, "%d.%d", &hasUnea1, &hasUnea12);
		orig_h1[strlen(orig_h1)] = '\0';
		resp_h1[strlen(resp_h1)] = '\0';
		service1[strlen(service1)] = '\0';
		flag1[strlen(flag1)] = '\0';
		
		//azken 2 segunduetako konexioak
		sartuDa2=0;
		count=0;
		serror=0;
		rerror=0;
		same_srv=0;
		diff_srv=0;
		srv_count=0;
		srv_serror=0;
		srv_error=0;
		srv_diff_host=0;
		for(j=nondik2; j<noraino; j++){
			strcpy(line2, inigo[j]);
			sscanf(line2, "%d %s %d %d %s %s %s %s %s %s %s",
			      		&konZenb2,&hasUnea2s,&orig_p2,&resp_p2,&orig_h2,&resp_h2,
					&duration2,&protokoloa2,&service2,&flag2);
			sscanf(hasUnea2s, "%d.%d", &hasUnea2, &hasUnea22);
			orig_h2[strlen(orig_h2)] = '\0';
			resp_h2[strlen(resp_h2)] = '\0';
			service2[strlen(service2)] = '\0';
			flag2[strlen(flag2)] = '\0';
			if((hasUnea1-2)<=hasUnea2 && hasUnea2<=hasUnea1){
				if(sartuDa2==0){ 
					nondik2=j;
					sartuDa2=1;
				}
				if (strcmp(resp_h1,resp_h2)==0){
					count= count + 1;
					if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
						serror= serror + 1;
					}
					if (strcmp(flag2,"REJ")==0){
						rerror= rerror + 1;
					}
					if (strcmp(service2,"other")!=0 && strcmp(service1,service2)==0){
						same_srv= same_srv + 1;
					}
					if (strcmp(service1,service2)!=0){
						diff_srv= diff_srv + 1;
					}	
				}
				if (resp_p1==resp_p2){
					srv_count= srv_count + 1;
					if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
						srv_serror= srv_serror + 1;
					}
					if (strcmp(flag2,"REJ")==0){
						srv_error= srv_error + 1;
					}
					if (strcmp(resp_h1,resp_h2)!=0){
						srv_diff_host= srv_diff_host + 1;
					}
				}				
			}
		}
		if (count!=0){
			serror_rate=(float)serror/(float)count;
			rerror_rate=(float)rerror/(float)count;
			same_srv_rate=(float)same_srv/(float)count;
			diff_srv_rate=(float)diff_srv/(float)count;
		}
		else{
			serror_rate= (float)0;
			rerror_rate= (float)0;
			same_srv_rate= (float)0;
			diff_srv_rate= (float)0;
		}
		if (srv_count!=0){
			srv_serror_rate=(float)srv_serror/(float)srv_count;
			srv_error_rate=(float)srv_error/(float)srv_count;
			srv_diff_host_rate=(float)srv_diff_host/(float)srv_count;
		}
		else{
			srv_serror_rate= (float)0;
			srv_error_rate= (float)0;
			srv_diff_host_rate= (float)0;
		}
		sprintf(line, "%s %d %d %f %f %f %f %f %f %f", 
							line1, 
							count,srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_error_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate);
		line[strlen(line)] = '\0';
		strcpy(inigo[noraino],line);

		//azken 100 konexioak
		if(noraino<=100){
			nondik100=0;
		}
		else{
			nondik100=noraino-100;
		}
		count=0;
		serror=0;
		rerror=0;
		same_srv=0;
		diff_srv=0;
		srv_count=0;
		srv_serror=0;
		srv_error=0;
		srv_diff_host=0;
		same_src_port=0;
		for(j=nondik100; j<noraino; j++){
			strcpy(line2, inigo[j]);
		  sscanf(line2, "%d %s %d %d %s %s %s %s %s %s %s",
		 		&konZenb2,&hasUnea2s,&orig_p2,&resp_p2,&orig_h2,&resp_h2,
		           	&duration2,&protokoloa2,&service2,&flag2);
		 	sscanf(hasUnea2s, "%d.%d", &hasUnea2, &hasUnea22);
		  orig_h2[strlen(orig_h2)] = '\0';
		  resp_h2[strlen(resp_h2)] = '\0';
		  service2[strlen(service2)] = '\0';
		  flag2[strlen(flag2)] = '\0';

			if (strcmp(resp_h1,resp_h2)==0){
      	count= count + 1;
        if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
        	serror= serror + 1;
        }
      	if (strcmp(flag2,"REJ")==0){
      		rerror= rerror + 1;
      	}
        if (strcmp(service2,"other")!=0 && strcmp(service1,service2)==0){
         	same_srv= same_srv + 1;
       	}
        if (strcmp(service1,service2)!=0){
          diff_srv= diff_srv + 1;
        }
   		}
			if (resp_p1==resp_p2){
     		srv_count= srv_count + 1;
        if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
        	srv_serror= srv_serror + 1;
       	}
        if (strcmp(flag2,"REJ")==0){
        	srv_error= srv_error + 1;
        }
        if (strcmp(resp_h1,resp_h2)!=0){
      		srv_diff_host= srv_diff_host + 1;
       	}
    	}
    	if (orig_p1==orig_p2){
    		same_src_port= same_src_port + 1;
    	}
		}
    if (count!=0){
      serror_rate=(float)serror/(float)count;
      rerror_rate=(float)rerror/(float)count;
      same_srv_rate=(float)same_srv/(float)count;
    	diff_srv_rate=(float)diff_srv/(float)count;
    }
    else{
    	serror_rate= (float)0;
      rerror_rate= (float)0;
      same_srv_rate= (float)0;
     	diff_srv_rate= (float)0;
   	}
		if (srv_count!=0){
			srv_serror_rate=(float)srv_serror/(float)srv_count;
		  srv_rerror_rate=(float)srv_error/(float)srv_count;
		  srv_diff_host_rate=(float)srv_diff_host/(float)srv_count;
		}
		else{
			srv_serror_rate= (float)0;
		  srv_rerror_rate= (float)0;
		  srv_diff_host_rate= (float)0;
		}
		if(noraino-nondik100!=0)
			same_src_port_rate=(float)same_src_port/(float)(noraino-nondik100);
		else
			same_src_port_rate=(float)0;

		strcpy(line1, inigo[noraino]);
    sprintf(line, "%s %d %d %f %f %f %f %f %f %f %f",
          		line1,    					count,srv_count,same_srv_rate,diff_srv_rate,same_src_port_rate,srv_diff_host_rate,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate);
  	line[strlen(line)] = '\0';
   	strcpy(inigo[noraino],line);
	}
	
	//idatzi trafAldagaiak
	sprintf(galdera, "trafAld.arff");
	ftrafAld = fopen(galdera, "w");	
	sprintf(galdera1, "countpacket.txt");
	attri = fopen(galdera1, "w");
	iicmp = iudp = itcp = 0;
	//Attributes
	for (i=0;i<countatt-1;i++){
		fprintf(ftrafAld, "%s",attributes[i]);
	}
	for(i=0; i<inigoKop; i++){	
		strcpy(linen,inigo[i]);
		count=0;
		point=0;
		fph=0;
		lph=0;
		while (count != 4){
			if (linen[fph]==' ') {
				count+=1;
				fph+=1;}
			else fph+=1;
		}
		lph=fph;
		count=0;
		while (count != 5){
			if (linen[lph]==' ') {
				count+=1;
				lph+=1;}
			else lph+=1;
		}
		for(j=fph;j<lph;j++){
			if (linen[j]==' ') filetoHong[j-fph]=','; 			
			else filetoHong[j-fph]=linen[j];
		}
		filetoHong[lph-fph-1]='\0';		
		count=0;
		j=0;
		while (j<strlen(linen)){
			if (linen[j]==' ') {
				linen[j]=ph;	
				count++;
				if (count == 6) point=j;	
			}
			j++;		
		}
		// Length of string
		length=strlen(linen)-point;
		//delete unnecessary attributes		
		for(j=0;j<strlen(linen)-point;j++){
			linen[j]=linen[j+point+1];
		}
		
		//find protocol
		ph1=0;
		while (linen[ph1] != ','){
			ph1++;
		}
		ph1++;		
		ph2=ph1;
		while (linen[ph2]!=','){
			ph2++;
		}
		for(j=ph1;j<ph2;j++){
			 protocol[j-ph1]=linen[j];
		}
		protocol[ph2-ph1]='\0';
		ph2++;		
		j=ph2;
		while (linen[ph2]!=','){
			port[ph2-j]=linen[ph2];
			ph2++;
		}
		port[ph2-j]='\0'; 
		iport = atoi(port);
		//Check services
		check = 1;
		if (iport == 5190) {strcpy(services,"aol"); check=0;}
		if (iport == 113) {strcpy(services,"auth");check=0;}
		if (iport == 179) {strcpy(services,"bgp");check=0;}
		if (iport == 530) {strcpy(services,"courier");check=0;}
		if (iport == 105) {strcpy(services,"csnet_ns");check=0;}
		if (iport == 84) {strcpy(services,"ctf");check=0;}
		if (iport == 13) {strcpy(services,"daytime");check=0;}
		if (iport == 9) {strcpy(services,"discard");check=0;}
		if (iport == 53) {strcpy(services,"domain");check=0;}
		if (iport == 1233) {strcpy(services,"domain_u");check=0;}
		if (iport == 7) {strcpy(services,"echo");check=0;}
		if (iport == 8) {strcpy(services,"eco_i");check=0;}
		if (iport == 0) {strcpy(services,"ecr_i");check=0;}
		if (iport == 520) {strcpy(services,"efs");check=0;}
		if (iport == 512) {strcpy(services,"exec");check=0;}
		if (iport == 79) {strcpy(services,"finger");check=0;}
		if (iport == 21) {strcpy(services,"ftp");check=0;}
		if (iport == 20) {strcpy(services,"ftp_data");check=0;}
		if (iport == 70) {strcpy(services,"gopher");check=0;}
		if (iport == 0) {strcpy(services,"harvest");check=0;}
		if (iport == 101) {strcpy(services,"hostnames");check=0;}
		if (iport == 80) {strcpy(services,"http");check=0;}
		if (iport == 2784) {strcpy(services,"http_2784");check=0;}
		if (iport == 443) {strcpy(services,"http_443");check=0;}
		if (iport == 8001) {strcpy(services,"http_8001");check=0;}
		if (iport == 993) {strcpy(services,"imap4");check=0;}
		if (iport == 529) {strcpy(services,"IRC");check=0;}
		if (iport == 102) {strcpy(services,"iso_tsap");check=0;}
		if (iport == 543) {strcpy(services,"klogin");check=0;}
		if (iport == 544) {strcpy(services,"kshell");check=0;}
		if (iport == 636) {strcpy(services,"ldap");check=0;}
		if (iport == 245) {strcpy(services,"link");check=0;}
		if (iport == 513) {strcpy(services,"login");check=0;}
		if (iport == 1911) {strcpy(services,"mtp");check=0;}
		if (iport == 42) {strcpy(services,"name");check=0;}
		if (iport == 138) {strcpy(services,"netbios_dgm");check=0;}
		if (iport == 137) {strcpy(services,"netbios_ns");check=0;}
		if (iport == 139) {strcpy(services,"netbios_ssn");check=0;}
		if (iport == 15) {strcpy(services,"netstat");check=0;}
		if (iport == 433) {strcpy(services,"nnsp");check=0;}
		if (iport == 119) {strcpy(services,"nntp");check=0;}
		if (iport == 123) {strcpy(services,"ntp_u");check=0;}
		if (iport == 5432) {strcpy(services,"pm_dump");check=0;}
		if (iport == 109) {strcpy(services,"pop_2");check=0;}
		if (iport == 110) {strcpy(services,"pop_3");check=0;}
		if (iport == 515) {strcpy(services,"printer");check=0;}
		if (iport == 5 && strcmp(protocol,"icmp") == 0) {strcpy(services,"red_i");check=0;}
		if (iport >= 71 && iport <= 74) {strcpy(services,"remote_job");}
		if (iport == 5 && (strcmp(protocol,"tcp") == 0) || (strcmp(protocol,"udp") == 0)) {strcpy(services,"rje");check=0;}
		if (iport == 514) {strcpy(services,"shell");check=0;}
		if (iport == 25) {strcpy(services,"smtp");check=0;}
		if (iport == 66) {strcpy(services,"sql_net");check=0;}
		if (iport == 22) {strcpy(services,"ssh");check=0;}
		if (iport == 111) {strcpy(services,"sunrpc");check=0;}
		if (iport == 95) {strcpy(services,"supdup");check=0;}
		if (iport == 11 && (strcmp(protocol,"tcp") == 0 || strcmp(protocol,"udp") == 0)) {strcpy(services,"systat");check=0;}
		if (iport == 23) {strcpy(services,"telnet");check=0;}
		if (iport == 69) {strcpy(services,"tftp_u");check=0;}
		if (iport == 13 && strcmp(protocol,"icmp") == 0) {strcpy(services,"tim_i");check=0;}
		if (iport == 37) {strcpy(services,"time");check=0;}
		if (iport == 3) {strcpy(services,"urh_i");check=0;}
		if (iport == 11 && strcmp(protocol,"icmp") == 0) {strcpy(services,"urp_i");check=0;}
		if (iport == 540) {strcpy(services,"uucp");check=0;}
		if (iport == 117) {strcpy(services,"uucp_path");check=0;}
		if (iport == 175) {strcpy(services,"vmnet");check=0;}
		if (iport == 43) {strcpy(services,"whois");check=0;}
		if (iport >= 6000 && iport <= 6063) {strcpy(services,"X11");check=0;}
		if (iport == 210) {strcpy(services,"Z39_50");check=0;}
		if (iport > 49151 && iport < 65535) {strcpy(services,"private");check=0;}
		if (check == 1) strcpy(services,"other"); 
		///////////
		//print to screen
		fprintf(attri, "%s,%s\n", filetoHong,services);
		while (linen[ph1]!=','){
			ph1++;
		} 
		ph2=ph1+1;
		while (linen[ph2]!=','){
			ph2++;
		}
		count=0;
		//Add string before services
		for(j=0;j<=ph1;j++){
			templine[j]=linen[j];
			count++;		
		}
		//add service to String
		for(j=count;j<count+strlen(services);j++){
			templine[j]=services[j-count];
		}
		count=count+strlen(services);
		for(j=ph2;j<strlen(linen);j++){
			templine[count+j-ph2]=linen[j];
		}
		length=strlen(linen)+strlen(services)-ph2+1+ph1;
		templine[length]='\0';
		if (strcmp(protocol,"tcp")==0) itcp++;
		if (strcmp(protocol,"udp")==0) iudp++;
		if (strcmp(protocol,"icmp")==0) iicmp++;
		fprintf(ftrafAld, "%s\n",templine);
	}
	//fprintf(ftrafAld, "%d || tcp: %d || udp: %d || icmp: %d \n",inigoKop,itcp,iudp,iicmp);
	fclose(ftrafAld);	
	
	//sprintf(galdera, "countpacket.txt");
	//attri = fopen(galdera, "w");
	fprintf(attri,"%d\n",inigoKop);
	fprintf(attri,"%d\n",itcp);	
	fprintf(attri,"%d\n",iudp);	
	fprintf(attri,"%d",iicmp);
	fclose(attri);
	//for(i=0; i<inigoKop; i++){
	//	fprintf(attri, "%s\n", inigo[i]);
	//}		
  	//fclose(attri);
}
