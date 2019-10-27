import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class dbServer {

    private static final String DATABASEURL = "c4g_db";

    public static void main (String[] args) throws SQLException {

        if(args.length != 2){
            System.out.println("Usage: java -classpath sqlite-jdbc.jar:javax.json-1.0.jar dbServer <action> <parameter>");
            System.exit(0);
        }
        else {
            Communicator communicator = new Communicator();
            Connection connection = DriverManager.getConnection("jdbc:sqlite:" + DATABASEURL);
            switch (args[0]) {
                case "create": {
                    communicator.createTables(connection);
                    break;
                }
                case "newAccount": {
                    communicator.newAccount(connection,args[1]);
                    break;
                }
                case "search": {
                    try{
                        communicator.search(connection,args[1]);
                    }catch (IOException e){
                        System.out.println(e.getMessage());
                    }
                    break;
                }
                case "addReason": {
                    communicator.addReason(connection,args[1]);
                    break;
                }
            }
            if (connection != null)
                connection.close();
        }
    }

}
