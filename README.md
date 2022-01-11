# Red-Eye-Removal

### Abstract:
The red-eye effect is typically produced by consumer  photos taken with the  built-in camera flash. Section presents a new algorithm for automatically removing red-eye from digital photography. The proposed algorithm can automatically remove red eyes without manual intervention. First, it uses the Cascade Classifier algorithm to recognize the  plane. The red eye is then placed using segmentation operations, morphology, and geometric constraints. Finally,  completely corrects the red eye found. The experimental results of the are satisfied with the high correction factor, the relatively low  computational complexity of the , and the robustness.
<br><br>
### Objective of the Work
To make a flawless red-eye removing algorithm
<br><br>
### Results
<table>
  <tr>
    <th>
    </th>
    <th>
      MSE
    </th>
    <th>
      PSNR
    </th>
    <th>
      SSIM
    </th>
  </tr>
  
  <tr>
    <th>
      Base Paper
    </th>
    <td>
      5.452
    </td>
    <td>
      42.633
    </td>
    <td>
      0.9757
    </td>
  </tr>
  
  <tr>
    <th>
      Proposed Alogrithm
    </th>
    <td>
      8.536
    </td>
    <td>
      40.466
    </td>
    <td>
      0.9622
    </td>
  </tr>
</table>
<br><br>

### CONCLUSIONS AND FUTURE WORK
Automatic red eye removal algorithm has been presented based on the Cascade Classifier algorithm. The experimental results are satisfied with high PSNR rates, relatively low Mean Square Error as mentioned in table1. The next step will focus on improving the performance of feature detection. The results show that the result of the base paper is better than our work but close.

