## Codebook for Covid-19 Policy Stringency Index for Germany
This codebook is constructed on the basis of the federal policies for contact restrictions that we have collected to calculate the Stringency Indices. The dataset that we have collected consists of 9 indicators that have been divided into 3 main groups:
- [E: Containment policies for schools](#containment-policies-for-schools)
- [S: Containment policies for entertainment and shopping (public activities)](#containment-policies-for-public-activities)
- [R: Containment policies for private gatherings](#containment-policies-for-private-gatherings)
<p align="justify">
All the 9 indicators are recorded on an ordinal scale according to the level of policy stringency. A value of 0 always indicates no contact restriction; values of 1 or larger represent an increase in the policy’s level of contact stringency. The data set further assigns each policy entry three additional values, namely two binary variables, the flag and the recorded flag, as well as the maximum value of the policy’s affiliated indicator. While the flag variable distinguishes between indicators that are not characterized by their geographic scope (0) and those that are (1), the recorded flag indicates whether an indicator was implemented at the state (0) or national (1) level.
</p>

---
### Containment policies for schools

| ID | Name | Description | Measurement | Coding |
| :--- | :--- | :--- | :--- | :--- |
| E1 | `SI_E1` | Record closings of kitas | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions)<br/>2 - closed<br/>-100 - no data |
| | `flag_E1` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_E1` | | Binary flag for policy implementation | 0 - state level<br/>1 - national level<br/>-100 - no data |
| E2 | `SI_E2` | Record closings of elementary schools | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions) <br/>2 - partially open<br/>3 - closed<br/>-100 - no data |
| | `flag_E2` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_E2` | | Binary flag for policy implementation| 0 - state level<br/>1 - national level<br/>-100 - no data |
| E3 | `SI_E3` | Record closings of schools for grades 5 to 10 | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions)<br/>2 - partially open<br/>3 - closed<br/>-100:no data |
| | `flag_E3` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_E3` | | Binary flag for policy implementation | 0 - state level<br/>1 - national level<br/>-100 - no data |
| E4 | `SI_E4` | Record closings of schools for grades 11 to 12/13 | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions)<br/>2 - partially open<br/>3 - closed<br/>-100 - no data |
| | `flag_E4` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_E4` | | Binary flag for policy implementation | 0 - state level<br/>1 - national level<br/>-100 - no data |

---
### Containment policies for public activities

| ID | Name | Description | Measurement | Coding |
| :--- | :--- | :--- | :--- | :--- |
| S1 | `SI_S1` | Record restrictions on stores | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions)<br/>2 - partially closed (>=800m2<br/>3 - closed<br/>-100 - no data |
| | `flag_S1` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_E1` | | Binary flag for policy implementation | 0 - state level<br/>1 - national level<br/>-100 - no data |
| S2 | `SI_S2` | Record restrictions on restaurants  | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions) <br/>2 - partially closed (takeaways allowed)<br/>3 - closed<br/>-100 - no data |
| | `flag_S2` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_S2` | | Binary flag for policy implementation| 0 - state level<br/>1 - national level<br/>-100 - no data |
| S3 | `SI_S3` | Record restrictions on entertainment, sports facitlites and cultural institutions | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions)<br/>2 - closed<br/>-100:no data |
| | `flag_S3` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_S3` | | Binary flag for policy implementation | 0 - state level<br/>1 - national level<br/>-100 - no data |
| S4 | `SI_S4` | Record restrictions on religious events | Ordinal scale | 0 - no measures<br/>1 - fully open (under certain hygenic and social distancing conditions)<br/>2 - closed<br/>-100 - no data |
| | `flag_S4` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_S4` | | Binary flag for policy implementation | 0 - state level<br/>1 - national level<br/>-100 - no data |

---
### Containment policies for private gatherings

| ID | Name | Description | Measurement | Coding |
| :--- | :--- | :--- | :--- | :--- |
| R1 | `R_index_score` | Record contact restrictions | Ordinal scale | 0 - no measures<br/>1 - contact reduced to <= 1000<br/>2 - contact reduced to <= 10 or 2 HH<br/>3 - contact reduced to 2 HH<br/>4 - contact reduced to gatherings of individuals from two hhs (total number of individuals may not exceed 10 individuals)<br/>5 - contact reduced to gatherings of individuals from two hhs (total number of individuals may not exceed 5 individuals)<br/>6 - contact reduced to <=4<br/>7 - contact limited to the members of one's HH and maximum of one individual from a different HH<br/>8 - contact reduced to the members of one's hh or maximum one individual from a different HH<br/>-100 - no data |
| | `flag_R1` | | Binary flag for geographic scope | 0 - targeted<br/>1 - general<br/>-100 - no data |
| | `recorded_flag_R1` | | Binary flag for policy implementation | 0 - state level<br/>1 - national level<br/>-100 - no data |

---
### Calculating Indicies

First we calculate the Sub Score Index for each of the 9 indicators. Then we calculate the individual stringency indices for three containment policy groups as well as the aggregate Stringency Index.

| Indicator | Max. value | Flag |
| :---: | :---: | :---: |
| E1 | 2(0,1,2) | yes=1 |
| E2 | 3(0,1,2,3) | yes=1 |
| E3 | 3(0,1,2,3) | yes=1 |
| E4 | 3(0,1,2,3) | yes=1 |
| S1 | 3(0,1,2,3) | yes=1 |
| S2 | 2(0,1,2) | yes=1 |
| S3 | 2(0,1,2) | yes=1 |
| S4 | 2(0,1,2) | yes=1 |
| R1 | 8(0,1,2,3,4,5,6,7,8) | yes=1 |

The Sub Score Index(_I_) for each indicator (_j_) and for each day (_t_), is calculated by the following formula:

\begin{equation}\label{eq:Eq1}
  I_{j,t} = 100\frac{v_{j,t} - 0.5\left(F_j - f_{j,t}\right)}{N_j}
\end{equation}

where,
- _N<sub>j</sub>_ is the maximum value of the indicator
- _F<sub>j</sub>_ is the flag value of the indicator
- _v<sub>j,t</sub>_ is the policy value on the ordinal scale
- _f<sub>j,t</sub>_ is the recorded flag value of the indicator

A simple average of the computed Sub Score Indices associated with each containment policy group yields the respective stringency index. By calculating the average of all indicators from the three containment policy groups, we derive the aggregated **Stringency Index**.

| Index name | _k_ | `SI_E1` | `SI_E2` | `SI_E3` | `SI_E4` | `SI_S1` | `SI_S2` | `SI_S3` | `SI_S4` | `R_index_Score` |
| :---: | :---: | :---: | :---: | :---: | :---: |:---: | :---: | :---: | :---: | :---: |
| `E_index_Score` | 4 | `x` | `x` | `x` | `x` | |  |  |  |  |
| `S_index_Score` | 4 |  |  |  |  | `x` | `x` | `x` | `x` | |
| `R_index_Score` | 1 |  |  | |  |  |  |  |  | `x` |
| `stringency_index_score`| 9 | `x` | `x` | `x` | `x` | `x` | `x` | `x`| `x`|  `x` |
