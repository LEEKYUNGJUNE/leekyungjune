package ai.mindslab.util;

import java.io.Reader;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class SqlSessionManager {
	
	private static SqlSession sqlSession;

	private SqlSessionManager() {
	}
	
	public static SqlSession getSqlSession() {
		if (sqlSession == null) {
			try {
				String resource = "mybatis/mysql-config.xml";
				Reader reader = Resources.getResourceAsReader(resource);
				SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);

				sqlSession = sqlSessionFactory.openSession();

			} catch (Exception e) {
				e.printStackTrace();
				throw new RuntimeException(e);
			}
		}
		return sqlSession;
	}

	public static void closeSqlSession() {
		sqlSession.close();
		sqlSession = null;
	}

}
