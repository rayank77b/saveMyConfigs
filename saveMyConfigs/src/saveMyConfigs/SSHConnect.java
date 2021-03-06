package saveMyConfigs;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;

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
	
	public void readSFTPChannel(String remotePath, ChannelSftp sftpChannel) throws SftpException, IOException {
		InputStream out= null;
        out= sftpChannel.get(remotePath);
        BufferedReader br = new BufferedReader(new InputStreamReader(out));
        String line;
        while ((line = br.readLine()) != null)
            System.out.println(line);
        br.close();
	}
	
	public void copyFileSFTPChannel(String remotePath, String localPath, ChannelSftp sftpChannel) throws IOException, SftpException {
	    InputStream is = null;
	    OutputStream os = null;
	    try {
	        is = sftpChannel.get(remotePath);
	        BufferedReader br = new BufferedReader(new InputStreamReader(is));
	        os = new FileOutputStream(new File(localPath));
	        byte[] buffer = new byte[1024];
	        int length;
	        while ((length = is.read(buffer)) > 0) {
	            os.write(buffer, 0, length);
	        }
	    } finally {
	        is.close();
	        os.close();
	    }
	}
}
