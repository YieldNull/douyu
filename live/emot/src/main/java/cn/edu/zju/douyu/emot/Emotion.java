package cn.edu.zju.douyu.emot;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.wltea.analyzer.cfg.DefaultConfig;
import org.wltea.analyzer.dic.Dictionary;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Emotion {
    private ConcurrentHashMap<String, Integer> dic;
    private ConcurrentHashMap<String, Double> adj;
    private Set<String> privatives;
    Analyzer anal;

    public Emotion() {
        dic = new ConcurrentHashMap<String, Integer>();
        adj = new ConcurrentHashMap<String, Double>();
        privatives = new HashSet<String>();
        Analyzer anal = new IKAnalyzer(true);
        //BufferedReader是可以按行读取文件
        try {
            InputStream dicStream = Emotion.class.getResourceAsStream("/dic.csv");
            InputStream adjStream = Emotion.class.getResourceAsStream("/adj.csv");
            InputStream priStream = Emotion.class.getResourceAsStream("/pri.csv");

            BufferedReader dicReader = new BufferedReader(new InputStreamReader(dicStream));
            BufferedReader adjReader = new BufferedReader(new InputStreamReader(adjStream));
            BufferedReader priReader = new BufferedReader(new InputStreamReader(priStream));
            String tmp = null;
            while ((tmp = dicReader.readLine()) != null) {
                int index = tmp.indexOf(',');
                String text = tmp.substring(0, index);
                int value = Integer.parseInt(tmp.substring(index + 1, tmp.length()));
                dic.put(text, value);
            }
            while ((tmp = adjReader.readLine()) != null) {
                int index = tmp.indexOf(',');
                String text = tmp.substring(0, index);
                Double value = Double.parseDouble(tmp.substring(index + 1, tmp.length()));
                adj.put(text, value);
            }
            while ((tmp = priReader.readLine()) != null) {
                privatives.add(tmp);
            }
        } catch (IOException e) {
            System.out.println("读取文件出错");
        }
        dic.toString();
        adj.toString();
        privatives.toString();

    }

    public double GetEmotValue(String text) {
        List<String> list = Split(text);
        double value = 0;
        for (int i = 0; i < list.size(); i++) {
            String s = list.get(i);
            Integer var = dic.get(s);
            if (var != null) value = value + var;
        }
        for (int i = 0; i < list.size(); i++) {
            String s = list.get(i);
            Double var = adj.get(s);
            if (var != null) value = value * var;
        }
        for (int i = 0; i < list.size(); i++) {
            String s = list.get(i);
            if (privatives.contains(s)) value = value * (-1);
        }
        return value;
    }


    public ConcurrentHashMap<String, Integer> GetEmotDic() {
        return dic;
    }


    private List<String> Split(String text) {
        List<String> list = new ArrayList<String>();

        // 尚未初始化，因为第一次执行分词的时候才会初始化，为了在执行分此前手动添加额外的字典，需要先手动的初始化一下
        Dictionary.initial(DefaultConfig.getInstance());
        Dictionary.getSingleton().addWords(list);

        //创建分词对象
        Analyzer analyzer = new IKAnalyzer(false);
        StringReader reader = new StringReader(text);

        TokenStream ts = analyzer.tokenStream("", reader);
        CharTermAttribute term = ts.getAttribute(CharTermAttribute.class);
        //遍历分词数据
        try {
            while (ts.incrementToken()) {
                list.add(term.toString());
                //System.out.print(term.toString()+"|");
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            reader.close();
        }
        return list;
    }


    //0代表无情感，1代表正向，-1代表负向
    public int GetEmotPolarity(double value) {
        if (value > 0) {
            return 1;
        } else if (value < 0) {
            return -1;
        } else {
            return 0;
        }
    }

    public int GetEmotPolarity(String text) {
        double value = GetEmotValue(text);
        return GetEmotPolarity(value);
    }

}

