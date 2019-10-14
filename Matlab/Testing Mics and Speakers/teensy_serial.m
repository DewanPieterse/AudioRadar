s = serial("/dev/cu.usbmodem58711701");
s.BaudRate=9600;
s.InputBufferSize=1000000;
fopen(s);
fprintf(s,'c');
% data=fread(s,num_samples*2,'uint8').';
% fclose(s);
% delete(s);