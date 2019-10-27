
import java.io.StringReader;
import java.sql.*;
import javax.json.*;



public class Communicator {

    private final String DEFAULT = "";
    private static final String DATABASEURL = "c4g_db";

    public void Communicator(){}

    public void createTables(Connection connection) throws SQLException {

        Statement statement = connection.createStatement();
        statement.executeUpdate("DROP TABLE IF EXISTS reasons");
        statement.executeUpdate("DROP TABLE IF EXISTS suggestions");
        statement.executeUpdate("DROP TABLE IF EXISTS preference");
        statement.executeUpdate("DROP TABLE IF EXISTS sports");
        statement.executeUpdate("DROP TABLE IF EXISTS basicInfo");
        statement.executeUpdate("CREATE TABLE basicInfo (" +
                "clientID VARCHAR(50) PRIMARY KEY NOT NULL, " +
                "name VARCHAR(50), " +
                "location VARCHAR(50), " +
                "gender VARCHAR(20), " +
                "birthday DATE, " +
                "jobCat VARCHAR(50))");
        statement.executeUpdate("CREATE TABLE sports (" +
                "sportNum INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "sportName VARCHAR(50))");
        statement.executeUpdate("CREATE TABLE preference (" +
                "client VARCHAR(50), " +
                "sport INTEGER, " +
                "FOREIGN KEY (client) REFERENCES basicInfo (clientID) ON UPDATE CASCADE ON DELETE CASCADE, " +
                "FOREIGN KEY (sport) REFERENCES sports (sportNum) ON UPDATE CASCADE ON DELETE CASCADE)");
        statement.executeUpdate("CREATE TABLE suggestions (" +
                "suggNum INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "description VARCHAR(100), " +
                "timeMin SMALLINT(1440), " +
                "teamSport BOOLEAN, " +
                "costly BOOLEAN, " +
                "calPH SMALLINT(2000), " +
                "sport INTEGER, " +
                "FOREIGN KEY (sport) REFERENCES sports (sportNum) ON UPDATE CASCADE ON DELETE CASCADE)");
        statement.executeUpdate("CREATE TABLE reasons (" +
                "client VARCHAR(50), " +
                "suggestion INTEGER, " +
                "reason VARCHAR(50), " +
                "FOREIGN KEY (client) REFERENCES basicInfo (clientID) ON UPDATE CASCADE ON DELETE CASCADE, " +
                "FOREIGN KEY (suggestion) REFERENCES suggestions (suggNum) ON UPDATE CASCADE ON DELETE CASCADE)");
        statement.close();

        testValues(connection);
    }


    private void testValues(Connection connection) throws SQLException{

        addNewSport(connection,"Football");
        addNewSport(connection,"Slow_Running");
        addNewSport(connection,"Swimming");

        addSuggestion(connection,"What about a 5 km run?",30,false,false,557,"Slow_Running");
        addSuggestion(connection,"What about swimming for 1 km?",40,false,true,590,"Swimming");
        addSuggestion(connection,"What about play a full football game?",90,true,false,800,"Football");


        PreparedStatement statement = connection.prepareStatement("INSERT INTO basicInfo (clientID ,name, location, gender, birthday, jobCat) " +
                                                           "VALUES (?, ?, ?, ?, ?, ?)");

        statement.setString(1,"ABCDEFGH");
        statement.setString(2,"Tony");
        statement.setString(3,"Glasgow");
        statement.setString(4,"Male");
        statement.setDate(5,Date.valueOf("2000-03-16"));
        statement.setString(6,"Student");
        statement.executeUpdate();

        statement = connection.prepareStatement("INSERT INTO preference (client, sport) VALUES (?, ?)");
        addPreference(connection,"ABCDEFGH","Football");
        addPreference(connection,"ABCDEFGH","Swimming");



        statement.close();
    }



    public void newAccount(Connection connection, String info) throws SQLException{

        PreparedStatement statement = connection.prepareStatement("INSERT INTO basicInfo " +
                                                "(clientID ,name, location, gender, birthday, jobCat) VALUES (?, ?, ?, ?, ?, ?)");

        JsonReader reader = Json.createReader(new StringReader(info));
        JsonObject mainObj = reader.readObject();

        String clientID;
        if (mainObj.containsKey("clientID")) {
            clientID = mainObj.getString("clientID");
            if(clientID != null && !clientID.isEmpty())
                statement.setString(1, clientID);
            else
                throw new IllegalArgumentException("Need a valid client ID");
        }else
            throw new IllegalArgumentException("Need a client ID");

        String name = DEFAULT;
        if (mainObj.containsKey("name"))
            name = mainObj.getString("name");
        statement.setString(2,name);

        String location = DEFAULT;
        if (mainObj.containsKey("location"))
            location = mainObj.getString("location");
        statement.setString(3,location);


        String gender = DEFAULT;
        if (mainObj.containsKey("gender"))
            gender = mainObj.getString("gender");
        statement.setString(4,gender);

        if (mainObj.containsKey("birthday")) {
            String birthday = mainObj.getString("birthday");
            statement.setDate(5,Date.valueOf(birthday));
        }else
            statement.setDate(5,Date.valueOf("0001-01-01"));

        String jobCat = DEFAULT;
        if (mainObj.containsKey("jobCat"))
            jobCat = mainObj.getString("jobCat");
        statement.setString(6,jobCat);

        if (mainObj.containsKey("preferences")){
            JsonArray p = mainObj.getJsonArray("preferences");
            for (int i = 0; i < p.size(); i++) {
                addPreference(connection,clientID,""+p.get(i));
            }
        }

        statement.executeUpdate();
        statement.close();
    }

    private void addNewSport(Connection connection, String name) throws SQLException{
        PreparedStatement statement = connection.prepareStatement("INSERT INTO sports (sportName) VALUES (?)");
        statement.setString(1,name);
        statement.executeUpdate();
        statement.close();
    }

    private void addSuggestion(Connection connection, String description, int time, boolean team,  boolean cost, int calPH, String sport) throws  SQLException{
        PreparedStatement statement = connection.prepareStatement("INSERT INTO suggestions " +
                                                                    "(description, timeMin, teamSport, costly, calPH, sport) VALUES (?, ?, ?, ?, ?, ?)");
        statement.setString(1,description);
        statement.setInt(2, time);
        statement.setBoolean(3,team);
        statement.setBoolean(4,cost);
        statement.setInt(5, calPH);
        int sportNum = sportNumGetter(connection, sport);
        statement.setInt(6,sportNum);
        statement.executeUpdate();
        statement.close();
    }

    private int sportNumGetter(Connection connection, String name) throws SQLException{
        Statement statementQ = connection.createStatement();
        ResultSet resultSet = statementQ.executeQuery("SELECT sportNum FROM sports " +
                "WHERE sportName = \"" + name + "\"");
        return resultSet.getInt("sportNum");
    }

    private void addPreference(Connection connection, String clientID, String sport) throws SQLException{
        PreparedStatement statement = connection.prepareStatement("INSERT INTO preference (client, sport) VALUES (?, ?)");
        statement.setString(1,clientID);
        statement.setInt(2,sportNumGetter(connection,sport));
        statement.executeUpdate();
        statement.close();
    }

    public String search(Connection connection, String input) throws SQLException{
        String[] in = input.split(",");
        if(in.length != 2)
            throw new IllegalArgumentException("Use format \"clientID,timeLimitInMinute\" (no space)");
        Statement statementQ = connection.createStatement();
        ResultSet resultSet = statementQ.executeQuery("SELECT description FROM suggestions, preference " +
                                "WHERE suggestions.sport = preference.sport AND preference.client = \"" + in[0] +
                                        "\" AND suggestions.timeMin <= " + Integer.parseInt(in[1]));
        String result = "{ \"suggestions\" : [\"";
        while(resultSet.next()){
            result = result + resultSet.getString("description") + "\", \"";
        }
        result = result.substring(0,result.length()-3);
        result = result + "] }";
        return result;
    }

    public void addReason(Connection connection, String input) throws SQLException{
        String[] in = input.split(",");
        if(in.length != 3)
            throw new IllegalArgumentException("Use format \"clientID,suggestionContent,reason\" (no space)");
        PreparedStatement statement = connection.prepareStatement("INSERT INTO reasons " +
                "(client, suggestion, reason) VALUES (?, ?, ?)");
        statement.setString(1,in[0]);
        statement.setInt(2,suggNumGetter(connection,in[1]));
        statement.setString(3,in[2]);
        statement.executeUpdate();
        statement.close();
    }

    private int suggNumGetter(Connection connection, String description) throws SQLException{
        Statement statementQ = connection.createStatement();
        ResultSet resultSet = statementQ.executeQuery("SELECT suggNum FROM suggestions " +
                "WHERE description = \"" + description + "\"");
        return resultSet.getInt("suggNum");
    }

}
