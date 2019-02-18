import java.net.URL;
import org.apache.xmlrpc.client.*;

// Compile it with:
// $ CLASSPATH=./apache-xmlrpc-3.1.3/lib/xmlrpc-client-3.1.3.jar:./apache-xmlrpc-3.1.3/lib/xmlrpc-common-3.1.3.jar javac MultiRobot.java
//
// Run it with:
// $ CLASSPATH=./apache-xmlrpc-3.1.3/lib/xmlrpc-client-3.1.3.jar:./apache-xmlrpc-3.1.3/lib/xmlrpc-common-3.1.3.jar:./apache-xmlrpc-3.1.3/lib/ws-commons-util-1.0.2.jar:./ java MultiRobot

public class MultiRobot {
   public static void main (String [] args) {

      try {
	 XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
	 config.setServerURL(new URL("http://127.0.0.1:8000/RPC2"));
	 XmlRpcClient client = new XmlRpcClient();
	 client.setConfig(config);
         
	 while(true) {
		 Object[] params = new Object[]{};
		 Object result = client.execute("render", params);
		 System.out.println(result);

		 // look 
		 result = client.execute("look", params);
		 // note that result is a Java Object array

		 // think
		 
		 // act
		 Object[] actionlist = new Object[]{new Integer(0),new Integer(0), new Integer(4), new Integer(4)}; 
		 params = new Object[]{actionlist};
		 result= client.execute("step", params);

		 if ((boolean)(((Object[])result)[2]))  // if done
			 break;
	 }
      } catch (Exception exception) {
         System.err.println("JavaClient: " + exception);
      }
   }
}
