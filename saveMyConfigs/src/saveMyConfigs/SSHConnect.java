package saveMyConfigs;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpException;

/*
 *  Info see: 
 * http://stackoverflow.com/questions/3071760/ssh-connection-with-java
 * http://www.jcraft.com/jsch/
 */

public class SSHConnect {
	private JSch jsch;
	private Session session;
	private String user, password, host;

	public SSHConnect(String user, String password, String host)  {
		this.jsch = new JSch();
		this.user = user;
		this.password = password;
		this.host = host;
	}
	
	public void connect() throws JSchException{
		this.session = jsch.getSession(this.user, this.host, 22);
		session.setPassword(this.password);
        session.setConfig("StrictHostKeyChecking", "no");
		this.session.connect();
	}

	public ChannelSftp openSFTPChannel() throws JSchException {
		ChannelSftp sftpChannel = (ChannelSftp) this.session.openChannel("sftp");
        sftpChannel.connect();
        return sftpChannel;
	}
	
	public void readSFTPChannel(String remoteFile, ChannelSftp sftpChannel) throws SftpException, IOException {
		InputStream out= null;
        out= sftpChannel.get(remoteFile);
        BufferedReader br = new BufferedReader(new InputStreamReader(out));
        String line;
        while ((line = br.readLine()) != null)
            System.out.println(line);
        br.close();
	}
	
}
