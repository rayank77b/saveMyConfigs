package saveMyConfigs.config;

import java.util.Map;

public class ENV {
	private String fileNameIni;
	private Map<String, Host> hosts;
	/**
	 * @param fileNameIni
	 */
	public ENV(String fileNameIni) {
		this.fileNameIni = fileNameIni;
		
	}
	

}
