package saveMyConfigs.tests;

import static org.junit.Assert.fail;

import java.io.IOException;

import org.junit.Test;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.SftpException;

import saveMyConfigs.SSHConnect;

public class TestSSHConnect {

	@Test
	public void test() {
		// user blub with pass blubber must exist on localhost, for test
		SSHConnect sshc = new SSHConnect("blub", "blubber", "localhost");
		try {
			sshc.connect();
		} catch (JSchException e) {
			fail("cannot connect, errors on connect, maybe no user blub exist on localhost");
		}
		
		ChannelSftp csftp;
		
		try {
			csftp = sshc.openSFTPChannel();
			try {
				sshc.readSFTPChannel("/tmp/a.txt", csftp ); // /tmp/a.txt must exists on localhost
			} catch (SftpException | IOException e) {
				fail("problems on read");
			}
		} catch (JSchException e) {
			fail("cannot open sftp channel");
		}
		
		
		
	}

}
