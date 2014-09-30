/*==============================================================================

  Copyright (c) Kitware, Inc.

  See http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware, Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

#ifndef __qAppStyle_h
#define __qAppStyle_h

// Slicer includes
#include "qSlicerAppExport.h"
#include "qSlicerStyle.h"

class Q_SLICER_APP_EXPORT qAppStyle
  : public qSlicerStyle
{
  Q_OBJECT
public:
  /// Superclass typedef
  typedef qSlicerStyle Superclass;

  /// Constructors
  qAppStyle();
  virtual ~qAppStyle();

  /// Reimplemented to customize colors.
  /// \sa QStyle::standardPalette()
  virtual QPalette standardPalette() const;

  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawComplexControl()
  void drawComplexControl(ComplexControl control,
                          const QStyleOptionComplex* option,
                          QPainter* painter,
                          const QWidget* widget = 0)const;
  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawControl()
  virtual void drawControl(ControlElement element,
                           const QStyleOption* option,
                           QPainter* painter,
                           const QWidget* widget = 0 )const;

  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawPrimitive()
  virtual void drawPrimitive(PrimitiveElement element,
                             const QStyleOption* option,
                             QPainter* painter,
                             const QWidget* widget = 0 )const;

  /// Tweak the colors of some widgets.
  virtual QPalette tweakWidgetPalette(QPalette palette,
                                      const QWidget* widget)const;

  /// Reimplemented to apply styling to widgets.
  /// \sa QStyle::polish()
  virtual void polish(QWidget* widget);
  using Superclass::polish;
};

#endif
