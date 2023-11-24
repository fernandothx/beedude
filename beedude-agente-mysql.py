�
    �$ae�$  �                   ��  � d dl Z d dlZd dlmZ d dlZd dlZd dlmZ e j	        �
                    dd�  �          ej        �   �          d dlmZmZ dZ e j        dd	�
�  �         e j        �                    dddd�  �        Z ed�  �          ed�  �          ed�  �          eej        �                    �   �         �                    �   �         �  �        Zd� Zd� Zd� Zd� Zd� Zd� Z e�   �          dS )�    N)�sleep)�config�DJANGO_SETTINGS_MODULEzbeedude.settings)�Elemento�Item�
   z/opt/bee/beedude/tmpT)�exist_ok�opt�bee�beedude�tmpz$---> Desenvolvido por: Bee Solutionsz---> Autor: Fernando Almondesz---> Sistema: Beedudec                 �  � t          d�  �         t          d�  �        t          d�  �        t          d�  �        t          d�  �        t          d�  �        d�}d| � d	�}t          � d
�}	 t          j        j        di |��}|�                    d��  �        }|�                    |�  �         |�                    �   �         }t          |ddd��  �        5 }|r|d         �
                    �   �         ng }t          j        ||��  �        }	|	�                    �   �          |	�                    |�  �         d d d �  �         n# 1 swxY w Y   n3# t          j        j        $ r}
t          d|
� ��  �         Y d }
~
nd }
~
ww xY wdt!          �   �         v r|r|�                    �   �          dt!          �   �         v r*|�                    �   �         r|�                    �   �          d S d S d S # dt!          �   �         v r|r|�                    �   �          dt!          �   �         v r)|�                    �   �         r|�                    �   �          w w w xY w)NzI--> Iniciando conexao com o banco de dados do Zabbix (Tabela de Hosts)...�DB_HOST_ZABBIX�DB_PORT_ZABBIX�DB_NAME_ZABBIX�DB_USER_ZABBIX�DB_PASSWORD_ZABBIX��host�port�database�user�passworda  
        select ht.name host, ht.hostid,it.name item, it.itemid ,hu.value status,from_unixtime(hu.clock) horario,concat('1') as node from items it
        inner join hosts ht on (it.hostid = ht.hostid)
        inner join hosts_groups hg on (hg.hostid = ht.hostid)
        inner join hstgrp hst on (hst.groupid = hg.groupid)
        inner join (select itemid, max(clock) as max_clock from history_uint group by itemid) as max_hu on max_hu.itemid = it.itemid
        inner join history_uint hu on (hu.itemid = max_hu.itemid and max_hu.max_clock = hu.clock)
        where it.hostid in (select hostid from hosts where status = 0 and flags = 0) and it.key_ = 'icmpping' and hst.name in ('BEEDUDE')
        group by it.itemid, ht.name, ht.hostid, it.name, it.itemid, hu.value, horario, node limit z;
    �/tabela_hosts.csvT��
dictionary�w� �utf-8��newline�encodingr   ��
fieldnames�$Erro ao conectar ao banco de dados: �cursor�conexao� ��printr   r   �mysql�	connector�connectr&   �execute�fetchall�open�keys�csv�
DictWriter�writeheader�	writerows�Error�locals�close�is_connected)�nodes�conexao_banco�consulta_sql�nome_arquivo_csvr'   r&   �
resultados�arquivo_csv�colunas�escritor_csv�erros              �beedude-agente-mysql.py�conecta_zabbix_hostsrD      s�  � �	�
U�V�V�V� �'�(�(��'�(�(��+�,�,��'�(�(��/�0�0�� �M�	� di�	� 	� 	�L� �0�0�0����/�)�:�:�M�:�:�����4��0�0�����|�$�$�$� �_�_�&�&�
� �"�C��g�F�F�F� 	/�+�.8�@�j��m�(�(�*�*�*�b�G��>�+�'�J�J�J�L� �$�$�&�&�&� �"�"�:�.�.�.�	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/���� 	/� 	/� 	/� 	/��� �?� � =� =� =��;�T�;�;�<�<�<�<�<�<�<�<�����=����
 �v�x�x�� 	�F� 	��L�L�N�N�N����� � 	�W�%9�%9�%;�%;� 	��M�M�O�O�O�O�O�	� 	� 	� 	�� �v�x�x�� 	�F� 	��L�L�N�N�N����� � 	�W�%9�%9�%;�%;� 	��M�M�O�O�O�O�	� 	���sW   �*A(E �AD<�0E �<E � E �E �E �G �E8�E3�.G �3E8�8G �A"Ic                  �  � t          d�  �         t          d�  �        t          d�  �        t          d�  �        t          d�  �        t          d�  �        d�} d}t          � d	�}	 t          j        j        di | ��}|�                    d
��  �        }|�                    |�  �         |�                    �   �         }t          |ddd��  �        5 }|r|d         �
                    �   �         ng }t          j        ||��  �        }|�                    �   �          |�                    |�  �         d d d �  �         n# 1 swxY w Y   n3# t          j        j        $ r}	t          d|	� ��  �         Y d }	~	nd }	~	ww xY wdt!          �   �         v r|r|�                    �   �          dt!          �   �         v r*|�                    �   �         r|�                    �   �          d S d S d S # dt!          �   �         v r|r|�                    �   �          dt!          �   �         v r)|�                    �   �         r|�                    �   �          w w w xY w)NzI--> Iniciando conexao com o banco de dados do Zabbix (Tabela de Items)...r   r   r   r   r   r   a�  
        select ht.hostid as hostid,ht.name as host,it.itemid as itemid,it.name as item,
        coalesce(hu.value, 0) as valor,
        concat(CASE WHEN (it.name like '%status%' or it.name like '%Link down%') THEN coalesce(hu.value, '0') ELSE '0' END) AS status,
        coalesce(from_unixtime(hu.clock), '2000-01-01 00:00:00') AS horario
        from items it
        inner join hosts ht on (ht.hostid = it.hostid)
        inner join hosts_groups hg on (hg.hostid = ht.hostid)
        inner join hstgrp hst on (hst.groupid = hg.groupid)
        left join (select itemid, max(clock) as max_clock from history_uint group by itemid) AS max_hu ON max_hu.itemid = it.itemid
        left join history_uint hu on hu.itemid = max_hu.itemid and hu.clock = max_hu.max_clock
        where (it.name like '%Bits r%' or it.name like '%Bits s%' or it.name like '%gei_%' or it.name like '%status%')
        and it.name not like ('%IFALIAS%')
        and it.name not like '%Vlan%' and it.name not like '%vlan%'
        and it.name not like '%{#IFNAME}%' and it.name not like '%{#SNMPVALUE}%' and it.name not like '%Fan%'
        and ht.status = 0 and ht.flags != 2 and it.status = 0 and hst.name in ('BEEDUDE');
    �/tabela_items.csvTr   r   r   r   r    r   r#   r%   r&   r'   r(   r)   )
r;   r<   r=   r'   r&   r>   r?   r@   rA   rB   s
             rC   �conecta_zabbix_itemsrG   X   s�  � �	�
U�V�V�V� �'�(�(��'�(�(��+�,�,��'�(�(��/�0�0�� �M��L�& �0�0�0����/�)�:�:�M�:�:�����4��0�0�����|�$�$�$� �_�_�&�&�
� �"�C��g�F�F�F� 	/�+�.8�@�j��m�(�(�*�*�*�b�G��>�+�'�J�J�J�L� �$�$�&�&�&� �"�"�:�.�.�.�	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/� 	/���� 	/� 	/� 	/� 	/��� �?� � =� =� =��;�T�;�;�<�<�<�<�<�<�<�<�����=����
 �v�x�x�� 	�F� 	��L�L�N�N�N����� � 	�W�%9�%9�%;�%;� 	��M�M�O�O�O�O�O�	� 	� 	� 	�� �v�x�x�� 	�F� 	��L�L�N�N�N����� � 	�W�%9�%9�%;�%;� 	��M�M�O�O�O�O�	� 	���sW   �&A(E �AD8�,E �8D<�<E �?D<� E �G �E4�E/�*G �/E4�4G �A"H=c                  ��  � t           � d�} t          | dd��  �        5 }t          j        |d��  �        }|D ]�}t	          |�  �         d� }	  ||d         �  �        }n# t
          $ r d }Y nw xY w	  ||d	         �  �        }n# t
          $ r d }Y nw xY wt          j        �                    d
g|d         |d         |d         |d         ||d���  �        \  }}��	 d d d �  �         d S # 1 swxY w Y   d S )Nz/lista-hosts-edges.csv�rr   �r"   �;��	delimiterc                 �p   � 	 t           j        �                    | ��  �        S # t           j        $ r Y d S w xY w)N��codigo)r   �objects�get�DoesNotExistrO   s    rC   �get_elemento_instancez,importa_edges.<locals>.get_elemento_instance�   sF   � � �#�+�/�/�v�/�>�>�>���,�  �  �  ��4�4� ���s   �" �5�5�host_a�host_b�hostidrP   �label�status�node)rP   rX   rY   rZ   rU   rV   �rP   �defaults)	r   r0   r2   �
DictReaderr*   �KeyErrorr   rQ   �update_or_create)	�csv_file_path�file�
csv_reader�rowrT   �host_a_instance�host_b_instance�item�createds	            rC   �importa_edgesrh   �   s�  � ��2�2�2�M�	�m�S�7�	3�	3�	3� �t��^�D�C�8�8�8�
�� 	� 	�C��#�J�J�J� �  �  �'�"7�"7��H��"F�"F����� '� '� '�"&����'����'�"7�"7��H��"F�"F����� '� '� '�"&����'���� %�,�=�=� �z�!�(�m� ��\�!�(�m���K�-�-�� � >� 
� 
�M�D�'�'�%	�� � � � � � � � � � � ���� � � � � � sZ   �-C'�A�C'�A,�)C'�+A,�,C'�0B�C'�B�C'�B�AC'�'C+�.C+c                  �  � t          d�  �         t          � d�} t          | dd��  �        5 }t          j        |d��  �        }|D ]d}t
          j        �                    t          |d         �  �        t          |d         �  �        |d	         |d
         d|d         d���  �        \  }}�e	 d d d �  �         d S # 1 swxY w Y   d S )Nz'--> Importando atualizacao dos hosts...r   rI   r   rJ   �,rL   rW   r   rY   �   �horario)rP   rX   rY   rZ   rl   r[   )	r*   r   r0   r2   r]   r   rQ   r_   �int�r`   ra   rb   rc   rf   rg   s         rC   �importa_hostsro   �   s   � �	�
3�4�4�4��-�-�-�M�	�m�S�7�	3�	3�	3� �t��^�D�C�8�8�8�
�� 	� 	�C�$�,�=�=��3�x�=�)�)�!�#�h�-�0�0� ��[�!�(�m��"�9�~�� � >� 
� 
�M�D�'�'�	�� � � � � � � � � � � ���� � � � � � s   �A>B8�8B<�?B<c                  ��  � t          d�  �         t          � d�} t          | dd��  �        5 }t          j        |d��  �        }|D ]�}t
          j        �                    t          |d         �  �        t          |d         �  �        |d	         d
z   |d         z   |d         dk    r|d         nd|d         dk    r|d         nd|d         d���  �        \  }}��	 d d d �  �         d S # 1 swxY w Y   d S )Nz'--> Importando atualizacao dos items...rF   rI   r   rJ   rj   rL   �itemidr   z | rf   rY   �NULLrk   �valorr   rl   )rq   �nomerY   rs   rl   )rq   r\   )	r*   r   r0   r2   r]   r   rQ   r_   rm   rn   s         rC   �importa_itemsru   �   sU  � �	�
3�4�4�4��-�-�-�M�	�m�S�7�	3�	3�	3� �t��^�D�C�8�8�8�
�� 	� 	�C� �L�9�9��3�x�=�)�)�!�#�h�-�0�0���K�%�/�#�f�+�=�/2�8�}��/F�M�c�(�m�m�A�-0��\�V�-C�J�S��\�\��"�9�~�� � :� 
� 
�M�D�'�'�	�� � � � � � � � � � � ���� � � � � � s   �B,C&�&C*�-C*c                  �  � 	 t          d�  �         t          �   �          t          �   �          t          �   �          t	          �   �          t          d�  �         t          d�  �         t          d�  �         t          d�  �         ��)NTz--> Atualizando dados...zE
--------------------------------------------------------------------z2
--> Aguardando 10 segundos ate a nova consulta...r   )r*   rD   rG   ro   ru   r   r(   �    rC   �executa_atualizacaorx   �   s}   � �	��(�)�)�)������������������V�W�W�W��C�D�D�D��V�W�W�W��b�	�	�	�	rw   ) �osr2   �timer   �mysql.connectorr+   �django�decoupler   �environ�
setdefault�setup�grafo.modelsr   r   r:   �makedirs�path�joinr   r*   �listrQ   �all�values�	elementosrD   rG   rh   ro   ru   rx   r(   rw   rC   �<module>r�      s�  �� 	�	�	�	� 
�
�
�
� � � � � � � � � � � ���� � � � � � � �
� � �.�0B� C� C� C� ������ '� '� '� '� '� '� '� '� 	�� ���"�T� 2� 2� 2� 2��g�l�l�5�%��E�2�2�� ��,� -� -� -� ��%� &� &� &� ��� � � ��D��!�%�%�'�'�.�.�0�0�1�1�	�9� 9� 9�v@� @� @�F!� !� !�F� � �(� � �(� � � � � � � � � rw   